#####coding=utf-8

import urllib.request
import redis
import urllib.parse
import json
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import http.cookiejar


# /redis/cluster/23:1417694197540

def con():
    pool = redis.ConnectionPool(host='ap2.jd.local', port=5360, password='/redis/cluster/1:1803528818953446384')
    r = redis.StrictRedis(connection_pool=pool)
    r.set('foo', 'bar')
    print(r.get('foo'))


def submitOrder(sku):
    url = "http://kill.jd.com/" + sku
    #  url = "http://localhost/"
    for i in range(1, 3):
        # try:
        # headers = {
        #     'Cookie': r'__jdu=1451250143; __jda=122270672.303707471.1479459530.1479459530.1479459530.1; __jdb=122270672.3.303707471|1.1479459530; __jdc=122270672; __jdv=122270672|direct|-|none|-|1479459530030; o2-webp=false; _jrda=1; _jrdb=1479459533353; 3AB9D23F7A4B3C9B=CEBPYGRMU57LZ565CXRFTBJVBW3WEFGULQF5GFOTUMLXJMCIXBJYUIPM6COASLA2PQVFUHSYFA5AYYAYFNEJCZYBPU; TrackID=10KLK1tMX0X79pCkq7_3ROz1ANdyOPpYkQIUyBR1DGRIZgSod7Mc9heinuxnlW8_zqgasnw2m9tfDVMFdmkue-ZBuztnE25biR6qbXXYFOXg; pinId=ydNYJ_b65cn6JO5wjMDd9Q; pin=test_dongdong; unick=Y--___--Y; thor=03237F9332E58DE0431F787D320C39183977ABB429DE1534FDD778B81BE1F9C4D698E3EDBEBB16E83EA969988AA083FE63291D571DFAE1B6D925F8D0540F9B2849D908FC89C5480B3CEBB3844ACC83C1594667CEEA02F9353F1D7880B450F8E7CB433880FCD74AFCAC30112203067104530AB81C21BF1C767FB7D29CB6FF89A1BF968065504ADC925E503B30613BAFD2; _tp=5kfB47uSeV7jTJGynHixQA%3D%3D; _pst=test_dongdong; ceshi3.com=YijsjOW3oKV6QgtbZvhrPuGo3ZSyybrL56AXHjxl03w',
        #     'Host': r'kill.jd.com',
        #     'Connection': r'keep-alive'
        # }
        # request.add_header('User-Agent', r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
        # request.add_header('Connection', r'keep-alive')
        # request.add_header('ContentType', r'text/html')
        # request.add_header('Upgrade-Insecure-Requests', r'1')
        # request.add_header('Accept-Encoding', r'gzip, deflate')
        # request.add_header('Accept', r'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        cj = cookielib.CookieJar();
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
        request = urllib.request.Request(url)  # open=urlopen response.getcode() header=response.info()
        request.add_header('Host', r'kill.jd.com')
        request.add_header('Cookie',
                           r'__jdu=1451250143; __jda=122270672.303707471.1479459530.1479459530.1479459530.1; __jdb=122270672.3.303707471|1.1479459530; __jdc=122270672; __jdv=122270672|direct|-|none|-|1479459530030; o2-webp=false; _jrda=1; _jrdb=1479459533353; 3AB9D23F7A4B3C9B=CEBPYGRMU57LZ565CXRFTBJVBW3WEFGULQF5GFOTUMLXJMCIXBJYUIPM6COASLA2PQVFUHSYFA5AYYAYFNEJCZYBPU; TrackID=10KLK1tMX0X79pCkq7_3ROz1ANdyOPpYkQIUyBR1DGRIZgSod7Mc9heinuxnlW8_zqgasnw2m9tfDVMFdmkue-ZBuztnE25biR6qbXXYFOXg; pinId=ydNYJ_b65cn6JO5wjMDd9Q; pin=test_dongdong; unick=Y--___--Y; thor=03237F9332E58DE0431F787D320C39183977ABB429DE1534FDD778B81BE1F9C4D698E3EDBEBB16E83EA969988AA083FE63291D571DFAE1B6D925F8D0540F9B2849D908FC89C5480B3CEBB3844ACC83C1594667CEEA02F9353F1D7880B450F8E7CB433880FCD74AFCAC30112203067104530AB81C21BF1C767FB7D29CB6FF89A1BF968065504ADC925E503B30613BAFD2; _tp=5kfB47uSeV7jTJGynHixQA%3D%3D; _pst=test_dongdong; ceshi3.com=YijsjOW3oKV6QgtbZvhrPuGo3ZSyybrL56AXHjxl03w')
        request.add_header('Connection', r'keep-alive')
        response = urllib.request.urlopen(request, timeout=5)
        print(response.read().decode('utf-8'))
        # except:
        #     print("cannot submit order this time date:%s" % datetime.now())


def tick():
    print('Tick! The time is: %s' % datetime.now())


def kill(jsonStr):
    try:
        wareList = jsonStr["miaoShaList"]
        print(wareList)
        for ware in wareList:
            miaoShaPrice = float(ware["miaoShaPrice"])
            price = float(ware["jdPrice"])
            if (miaoShaPrice * 2.0 <= price):
                wareId = ware["wareId"]
                startTimeShow = ware["startTimeShow"]
                print(wareId)
                if __name__ == '__main__':
                    itime = datetime.now()
                    scheduler = BlockingScheduler()  # BlockingScheduler
                    scheduler.add_job(submitOrder, 'date',
                                      run_date=datetime(itime.year, itime.month, itime.day, int(18),
                                                        int(3), 0), args=[wareId])
                    # scheduler.add_job(submitOrder, 'interval', seconds=3, args=[wareId])
                    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
                    try:
                        scheduler.start()
                    except (KeyboardInterrupt, SystemExit):
                        scheduler.shutdown()
    except:
        print("seckill error !")
    return jsonStr


def getHtml(url):
    url = url + "&_=" + str(time.time())
    page = urllib.request.urlopen(url)
    try:
        html = page.read().decode('unicode_escape')
        length = len(html)
        jsonStr = json.loads(html[18:length - 2])
        wareList = jsonStr["miaoShaList"]
        print(wareList)
        for ware in wareList:
            miaoShaPrice = float(ware["miaoShaPrice"])
            price = float(ware["jdPrice"])
            if (miaoShaPrice * 2.0 <= price):
                wareId = ware["wareId"]
                itime = datetime.now()
                startTimeShow = ware["startTimeShow"]
                # if (itime.hour * 60 + itime.minute + 5 < int(startTimeShow[0:2]) * 60 + int(startTimeShow[3:5])):
                kill(jsonStr)
                # print(wareId)
    except:
        print("seckill error !")
    return jsonStr


def tickForJson(url):
    try:
        if __name__ == '__main__':
            scheduler = BlockingScheduler()  # BackgroundScheduler
            scheduler.add_job(getHtml, 'interval', seconds=1, args=[url])
            try:
                scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                scheduler.shutdown()
    except:
        print("seckill error !")


tickForJson("http://ai.jd.com/index_new?app=Seckill&action=pcMiaoShaAreaList&callback=pcMiaoShaAreaList")
