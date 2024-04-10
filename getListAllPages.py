from getVideoList import path,confirmCode,kotosi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wdw
import pandas as pd
import re
from time import sleep

def getUp():
    videos = browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]")
    aid = re.findall(r'data-aid=\"(.*?)\"',videos.get_attribute("innerHTML"))
    title = re.findall(r'alt=\"(.*?)\"',videos.get_attribute("innerHTML"))
    release = []
    for i in range(len(aid)):
        release.append(browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]/li[%d]/div/span[2]"%(i+1)).text)
    sleep(2)
    print(list(zip(title,aid,release)))
    return list(zip(title,aid,release))

def getAllVideos(link,browser):
    browser.get(link)
    tmp = confirmCode()
    allList = []
    endPage = eval(browser.find_element(By.XPATH,"/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[3]/span[1]").get_attribute('innerHTML').split()[1])
    page = 1
    allAid = []
    allTitle = []
    allRelease = []
    while tmp == '1':
        sleep(1)
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
        print("page {}".format(page))
        if page < endPage:browser.find_element(By.CLASS_NAME,"be-pager-next").click()
        else:break
        page += 1
    saveInfo = []
    allList = list(zip(allTitle,allAid,allRelease))
    for i in range(len(allList)):
        saveInfo.append([i,allList[i][0],allList[i][1],allList[i][2]])
    pd.DataFrame(saveInfo,columns=["主键","标题","BV","发布时间"]).to_excel(path+"/allList.xlsx",sheet_name="allList",index=False)

if __name__=='__main__':
    OPTIONS = webdriver.ChromeOptions()
    OPTIONS.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')
    browser = webdriver.Chrome(options=OPTIONS)
    link = "https://space.bilibili.com/267766441/video"
    getAllVideos(link,browser)
    browser.close()
