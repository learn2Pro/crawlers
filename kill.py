#####coding=utf-8

import urllib.request
import redis
import urllib.parse
import json
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os


# /redis/cluster/23:1417694197540

def con():
    pool = redis.ConnectionPool(host='ap2.jd.local', port=5360, password='/redis/cluster/1:1803528818953446384')
    r = redis.StrictRedis(connection_pool=pool)
    r.set('foo', 'bar')
    print(r.get('foo'))


def submitOrder(sku):
    url = "http://kill.jd.com/" + sku
    for i in range(1, 5):
        try:
            response = urllib.request.urlopen(url)
            print(response.read().decode('utf-8'))
        except:
            print("cannot submit order this time date:%s" % datetime.now())


def tick():
    print('Tick! The time is: %s' % datetime.now())


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
                startTimeShow = ware["startTimeShow"]
                print(wareId)
                if __name__ == '__main__':
                    itime = datetime.now()
                    scheduler = BlockingScheduler()
                    scheduler.add_job(submitOrder, 'date',
                                      run_date=datetime(itime.year, itime.month, itime.day, int(startTimeShow[0:2]),
                                                        int(startTimeShow[3:5]), 0),args=[wareId])
                    # scheduler.add_job(submitOrder, 'interval', seconds=3, args=[wareId])
                    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
                    try:
                        scheduler.start()
                    except (KeyboardInterrupt, SystemExit):
                        scheduler.shutdown()
    except:
        print("seckill error !")
    return jsonStr


html = getHtml("http://ai.jd.com/index_new?app=Seckill&action=pcMiaoShaAreaList&callback=pcMiaoShaAreaList")
