import requests
import re
import time
import csv
path = "/Users/pc/Desktop/桌面/danmakuAnalysis.nosync/test"
bv = "BV1C94y1p7yk"

#消息头信息
header={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

#获取评论API
original_url = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={}&type=1&oid={}&mode=3'

#时间戳转换成日期
def get_time(ctime):
    timeArray = time.localtime(ctime)
    otherStyleTime = time.strftime("%Y.%m.%d", timeArray)
    return str(otherStyleTime)

#获取aid
def get_oid(bvid):
    video_url = 'https://www.bilibili.com/video/' + bvid
    page = requests.get(video_url, headers=header).text
    aid = re.search(r'"aid":[0-9]+', page).group()[6:]
    return aid

#边爬取评论边保存文件
def online_save(Bvid):
    all_count = 0
    oid = get_oid(Bvid)
    page = 1
    url = original_url.format(page, oid)
    html = requests.get(url, headers=header)
    data = html.json()
    count = int(data['data']['cursor']['all_count'])
    fname = Bvid + '_评论.csv'
    with open(fname, 'w+', newline='', encoding='utf_8_sig') as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow(["时间", "点赞", "评论"])
        for i in data['data']['replies']:
            message=i['content']['message']
            message = re.sub('\s+', '', message)
            ctime=get_time(i['ctime'])
            like=i['like']
            csv_writer.writerow([ctime,str(like),message])
            all_count = all_count + 1
        print('总评论数：{}，当前评论数:{},爬取Page{}完毕。'.format(count, all_count, page))
        time.sleep(5)
        while all_count < count:
            page += 1
            url = original_url.format(page, oid)
            try:
                html = requests.get(url, headers=header)
                data = html.json()
                for i in data['data']['replies']:
                    message = i['content']['message']
                    ctime = get_time(i['ctime'])
                    like = i['like']
                    csv_writer.writerow([ctime, str(like), message])
                    # f.write(ctime+'\t' + str(like) + '\n')
                    # f.write(message)
                    # f.write('\n------------------------\n')
                    all_count = all_count + 1
                print('总评论数：{}，当前评论数:{},爬取Page{}完毕。'.format(count, all_count, page))
                time.sleep(5)
            except:
                break
        f.close()

if __name__=='__main__':
    Bvid=input('输入视频Bvid:')
    online_save(Bvid)
    print('完成！')



