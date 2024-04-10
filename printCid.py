# cid = 142635628
# danmakuUrl = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
# print(danmakuUrl)
import time
import pandas as pd
from xml.etree import ElementTree as et
import jieba
savePath="/Users/pc/Desktop/桌面/danmakuAnalysis.nosync/"
name = "人生第一次"
info = [name,"BV"]
with open("dm.txt") as f:
    xml = f.read()
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