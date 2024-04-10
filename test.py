import re

with open("/Users/pc/Desktop/桌面/danmakuAnalysis.nosync/html.txt") as fp:
    txts = fp.read()
aid = re.findall(r'data-aid=\"(.*?)\"',txts)
title = re.findall(r'alt=\"(.*?)\"',txts)
release = re.findall(r'<span class=\"time\">(.*?)</span>',txts)
print(release)
print(list(zip(aid,title)))