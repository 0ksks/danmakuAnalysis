from selenium.webdriver.common.by import By
import selenium.webdriver as wbd
import time
import pandas as pd
import sys

danmakuUrl = "https://live.bilibili.com/24492935?hotRank=0&session_id=27b90422114bf2ff0b99f6800f65236b_8191DBCD-A342-4080-8110-48ABD50E03C4&launch_id=1000238&live_from=71004"
dri = wbd.Chrome()
dri.get(danmakuUrl)
print("open successfully")
times = 0
endd = 10
while True:
    times+=1
    danmakuList = dri.find_elements(By.CLASS_NAME,"chat-items")
    if times > endd:
        break
    print("catching")
    time.sleep(2)
print(danmakuList[0].text)
dri.close()