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
    # req = urllib.request.Request("http://kill.jd.com/2918972.html")
    # req.add_header('User-Agent',r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
    # req.add_header('Host',r'kill.jd.com')
    # req.add_header('Cookie',r"__jdu=303707471; __jda=122270672.303707471.1479459530.1479878747.1479883379.18; __jdv=122270672|direct|-|none|-|1479459530030; _jrda=14; TrackID=18sWB8uYPslsle7dI4YSm67EV3MdI8xosVqTu3qFdXcm3v_pYJeaHSD2lszmMQ8-ZUECWXiEOZ70ufu9vM5Ty19YbIJhE5fAgeLur60LIBUE; pinId=ydNYJ_b65cn6JO5wjMDd9Q; unick=Y--___--Y; _tp=5kfB47uSeV7jTJGynHixQA%3D%3D; _pst=test_dongdong; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; __tra=122270672.925679695.1479795848.1479874489.1479885275.4; __trv=122270672%7Cdirect%7C-%7Cnone%7C-%7C1479884315949; __tru=46eede7f-1b01-4a11-998a-6b2aad773273; user-key=518b6134-9eef-43bc-8b7e-74edddab60a4; cn=59; erp1.jd.com=4550ADAFAF3EFB4294709A41AE8151BB9B55F7EE8DD44800F839BD8D96F23387CFC3AD1CEA6F3C070600FAEBE1549CFF12371E8BBFEF9D062F5FDC3B63C8E5A53933A376671B2747ED3877F21E2A73CF; __jdc=122270672; ceshi3.com=YijsjOW3oKV6QgtbZvhrPuGo3ZSyybrL56AXHjxl03w; _zhuangxiu_=RAGZY3S5JWKJ5EJFXYTM6MQMJEZTSXSI3YPFBELIYG3CUQUJEMQHKJKWC66SFX4FFBNSXGGVIQ7MA; sso.jd.com=901012e04a7d4a008fe0b9ee60ac1d5d; __trc=122270672; __jdb=122270672.28.303707471|18.1479883379; _jalc_=EJI5VS5LREJHSAYSEZJVNSGHKUSNRZWODARWBNCQTRFAKFMFAKH7YBCFNRDI6FJZM76KOULYNWCPD5AMAS7VRTFSJUPIY6QWB7QHFH7NH55DFERJI6TUR3VGQYLWXELR; _jshop_pop_=185bf5b435f1ae5a463115af4581628b; 3AB9D23F7A4B3C9B=CEBPYGRMU57LZ565CXRFTBJVBW3WEFGULQF5GFOTUMLXJMCIXBJYUIPM6COASLA2PQVFUHSYFA5AYYAYFNEJCZYBPU; pin=test_dongdong; thor=4842F5B521918CC05D4FEA7149F762CB4D733DC6C59BDAA3FB44B290ED7C666E1DDD7C68BF9B0870848DF2C006CC5A309AEB51FB4AE9BA9A0EEA54D2B4425B3EA70F91E832F32CEF29C6EF64CCC70157E77CAF44E1F80D2E5DA784C8638F8601DB3A963BAC7F65613C8580FD7EA3526E4822C0E91163015007A3AB4B9AB0D7955A0C0A7AE2B77DD5EEF5370802CEA397")
    # resp = urllib.request.urlopen(req)
    # html = resp.read()
    # print(html.decode('utf-8'))
    for i in range(1, 3):
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
            req.add_header('Host', r'kill.jd.com')
            req.add_header('Cookie',
                           r"__jdu=303707471; __jda=122270672.303707471.1479459530.1479878747.1479883379.18; __jdv=122270672|direct|-|none|-|1479459530030; _jrda=14; TrackID=18sWB8uYPslsle7dI4YSm67EV3MdI8xosVqTu3qFdXcm3v_pYJeaHSD2lszmMQ8-ZUECWXiEOZ70ufu9vM5Ty19YbIJhE5fAgeLur60LIBUE; pinId=ydNYJ_b65cn6JO5wjMDd9Q; unick=Y--___--Y; _tp=5kfB47uSeV7jTJGynHixQA%3D%3D; _pst=test_dongdong; ipLocation=%u5317%u4EAC; areaId=1; ipLoc-djd=1-72-2799-0; __tra=122270672.925679695.1479795848.1479874489.1479885275.4; __trv=122270672%7Cdirect%7C-%7Cnone%7C-%7C1479884315949; __tru=46eede7f-1b01-4a11-998a-6b2aad773273; user-key=518b6134-9eef-43bc-8b7e-74edddab60a4; cn=59; erp1.jd.com=4550ADAFAF3EFB4294709A41AE8151BB9B55F7EE8DD44800F839BD8D96F23387CFC3AD1CEA6F3C070600FAEBE1549CFF12371E8BBFEF9D062F5FDC3B63C8E5A53933A376671B2747ED3877F21E2A73CF; __jdc=122270672; ceshi3.com=YijsjOW3oKV6QgtbZvhrPuGo3ZSyybrL56AXHjxl03w; _zhuangxiu_=RAGZY3S5JWKJ5EJFXYTM6MQMJEZTSXSI3YPFBELIYG3CUQUJEMQHKJKWC66SFX4FFBNSXGGVIQ7MA; sso.jd.com=901012e04a7d4a008fe0b9ee60ac1d5d; __trc=122270672; __jdb=122270672.28.303707471|18.1479883379; _jalc_=EJI5VS5LREJHSAYSEZJVNSGHKUSNRZWODARWBNCQTRFAKFMFAKH7YBCFNRDI6FJZM76KOULYNWCPD5AMAS7VRTFSJUPIY6QWB7QHFH7NH55DFERJI6TUR3VGQYLWXELR; _jshop_pop_=185bf5b435f1ae5a463115af4581628b; 3AB9D23F7A4B3C9B=CEBPYGRMU57LZ565CXRFTBJVBW3WEFGULQF5GFOTUMLXJMCIXBJYUIPM6COASLA2PQVFUHSYFA5AYYAYFNEJCZYBPU; pin=test_dongdong; thor=4842F5B521918CC05D4FEA7149F762CB4D733DC6C59BDAA3FB44B290ED7C666E1DDD7C68BF9B0870848DF2C006CC5A309AEB51FB4AE9BA9A0EEA54D2B4425B3EA70F91E832F32CEF29C6EF64CCC70157E77CAF44E1F80D2E5DA784C8638F8601DB3A963BAC7F65613C8580FD7EA3526E4822C0E91163015007A3AB4B9AB0D7955A0C0A7AE2B77DD5EEF5370802CEA397")
            resp = urllib.request.urlopen(req)
            html = resp.read()
            print(html.decode('utf-8'))
        except:
            print("cannot submit order this time date:%s" % datetime.now())


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
                    scheduler = BackgroundScheduler()  # BlockingScheduler
                    scheduler.add_job(submitOrder, 'date',
                                      run_date=datetime(itime.year, itime.month, itime.day, int(startTimeShow[0:2]),
                                                        int(startTimeShow[3:5]), 0), args=[wareId])
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
                if (itime.hour * 60 + itime.minute + 5 < int(startTimeShow[0:2]) * 60 + int(startTimeShow[3:5])):
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
# submitOrder("3028491")