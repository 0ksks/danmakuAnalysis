import re
import requests
import time
import pandas as pd
from xml.etree import ElementTree as et
from selenium import webdriver
import os
import jieba
# video = "https://www.bilibili.com/video/BV1C94y1p7yk/?spm_id_from=333.1007.tianma.1-2-2.click&vd_source=d65473f5282c0a31ff7caf98e5d5f0f2"#视频链接
# req = requests.get(video)#获取response
# OPTIONS = webdriver.ChromeOptions()
# OPTIONS.add_argument(
#     'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')
# browser = webdriver.Chrome(options=OPTIONS)

def getDanmaku(info,savePath="/Users/pc/Desktop/桌面/danmakuAnalysis.nosync/"):
    if savePath!="/Users/pc/Desktop/桌面/danmakuAnalysis.nosync/":
        if not os.path.exists(savePath):os.mkdir(savePath)
        savePath = savePath + "/"
    name = info[0]
    video = info[1]
    video = "https://www.bilibili.com/video/"+video
    req = requests.get(video)#获取response
    html = req.text
    # cid = re.findall('\"cid\":(.*?),',html)[0]#从response中用正则表达式寻找cid（即该视频调用弹幕时向api接口发送的信息）
    cid = 1413799076
    danmakuUrl = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)#改为由本程序发送并获取弹幕
    # browser.get(danmakuUrl)
    # xml = browser.find_elements(By.CLASS_NAME,"pretty-print")[0].text
    xml = requests.get(danmakuUrl).content
    print(xml)
    tree = et.XML(xml)
    dm = tree.findall('d')
    res = []
    for i in range(7,len(dm)):#前6行内容为视频信息而非弹幕信息
        txt = dm[i].attrib['p'].split(',')
        realTimeStr=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(txt[4])))#弹幕发送的时间
        totalSec = int(txt[0].split('.')[0])#弹幕在视频中出现的时间(s)
        sec = totalSec%60
        minu = totalSec//60%60
        hour = totalSec//60//60
        videoTime="{}:{}:{}".format(hour,minu,sec)#转换时间格式
        res.append([i-7,realTimeStr.split()[0],realTimeStr.split()[1],videoTime,dm[i].text,jieba.lcut(dm[i].text),totalSec])#储存结果
    res.sort(key=lambda x:x[-1])#按照弹幕在视屏中出现的时间排序
    for i in res:
        i.pop()
    print(name+" saving...",end="")
    try:
        pd.DataFrame(res,columns=["主键","发送日期","发送时间","视频时间","内容","分词"]).to_excel(savePath+name.replace("/","\\")+".xlsx",sheet_name=info[1],index=False)#导入excel
        print("|saved")
    except Exception as error:
        print("|failed",error)
if __name__=='__main__':
    print("start")
    getDanmaku(["好笑么？用命换的","BV1aT4y1h71M"])
