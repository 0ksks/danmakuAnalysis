from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from pcapi import getDanmaku
import pandas as pd
import os

link = "https://space.bilibili.com/267766441/video"
path = "/Users/pc/Desktop/桌面/danmakuAnalysis.nosync/血狼破军"
account_password = ["13544005436","Llyyxx20030212!"]
kotosi = "2023"

def confirmCode():
    if EC.visibility_of_element_located((By.CLASS_NAME,"geetest-widget")):tmp = input("confirm code\n")
    return tmp

def getUp(link):
    browser.get(link)
    confirmCode()
    browser.find_element(By.XPATH,"/html/body/div[1]/div/div/ul[2]/li[1]/li/div/div").click()
    time.sleep(2)
    browser.find_element(By.XPATH,"/html/body/div[4]/div/div[4]/div[2]/form/div[1]/input").send_keys(account_password[0])
    browser.find_element(By.XPATH,"/html/body/div[4]/div/div[4]/div[2]/form/div[3]/input").send_keys(account_password[1])
    browser.find_element(By.XPATH,"/html/body/div[4]/div/div[4]/div[2]/div[2]/div[2]").click()
    confirmCode()
    videos = browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]")
    aid = re.findall(r'data-aid=\"(.*?)\"',videos.get_attribute("innerHTML"))
    title = re.findall(r'alt=\"(.*?)\"',videos.get_attribute("innerHTML"))
    release = []
    for i in range(len(aid)):
        release.append(browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]/li[%d]/div/span[2]"%(i+1)).text)
    time.sleep(2)
    return list(zip(title,aid,release))

def saveInfos(link,path):
    if not os.path.exists(path):os.mkdir(path)
    info = getUp(link)
    saveInfo = []
    for i in range(len(info)):
        saveInfo.append([i,info[i][0],info[i][1],info[i][2]])
    # pd.DataFrame(saveInfo,columns=["主键","标题","BV","发布时间"]).to_excel(path+"/list.xlsx",sheet_name="list",index=False)
    for i in range(10):
        getDanmaku(info[i],path)

if __name__=='__main__':
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')
    browser = webdriver.Chrome(options=OPTIONS)
    
    browser.get(link)
    tmp = confirmCode()
    allList = []
    endPage = eval(browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[3]/span[1]").get_attribute('innerHTML').split()[1])
    page = 1
    allAid = []
    allTitle = []
    allRelease = []
    while tmp == '1':
        time.sleep(1)
        videos = browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]")
        aid = re.findall(r'data-aid=\"(.*?)\"',videos.get_attribute("innerHTML"))
        title = re.findall(r'alt=\"(.*?)\"',videos.get_attribute("innerHTML"))
        release = []
        for i in range(len(aid)):
            tmptext = browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]/li[%d]/div/span[2]"%(i+1)).text
            savetext = tmptext.split("-")
            if len(savetext)==2:tmptext=kotosi+"-"+tmptext
            release.append(tmptext)
        allAid += aid
        allTitle += title
        allRelease += release
        print(release)
        if page < endPage:browser.find_element(By.CLASS_NAME,"be-pager-next").click()
        else:break
        page += 1
    saveInfo = []
    allList = list(zip(allTitle,allAid,allRelease))
    for i in range(len(allList)):
        saveInfo.append([i,allList[i][0],allList[i][1],allList[i][2]])
    pd.DataFrame(saveInfo,columns=["主键","标题","BV","发布时间"]).to_excel(path+"/allList.xlsx",sheet_name="allList",index=False)
    
    # getUp(link)