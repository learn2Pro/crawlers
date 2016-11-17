#####coding=utf-8

import re
import urllib.request
import sys
import redis
from urllib.error import URLError, HTTPError
import urllib.parse


# /redis/cluster/23:1417694197540

def con():
    pool = redis.ConnectionPool(host='ap2.jd.local', port=5360, password='/redis/cluster/1:1803528818953446384')
    r = redis.StrictRedis(connection_pool=pool)
    r.set('foo', 'bar')
    print(r.get('foo'))


# def findUrl(html):
#     reg = r'item.jd.com/(\w+)'
#     imgre = re.compile(reg)
#     imglist = re.findall(imgre, html)
#     x = 0
#     print(imglist)
#     for imgurl in imglist:
#         # imgurl = "http://kill.jd.com/" + imgurl
#         # page = urllib.request.urlopen(imgurl)
#         # response = page.read().decode('utf-8')
#         # print(response)
#         x += 1
#     print(x)
#
#
# def getHtml(url):
#     page = urllib.request.urlopen(url)
#     html = page.read().decode('utf-8')
#     return html

def findUrl(url):
    html = getHtml(url)
    x = isJd(html)
    print(x)
    if (x != 0):
        reg = r"((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)"
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        #  print(imglist)
        for imgurl in imglist:
            toUrl = imgurl[0]
            print(toUrl)
            if (isNotImg(toUrl) and not urlAborted(toUrl)):
                try:
                    x += findUrl(toUrl)
                except:
                    print("cannot add to x!!")
    else:
        return x;


def isJd(html):
    reg = r'jd.com'
    hasReg = re.compile(reg)
    list_length = len(re.findall(hasReg, html))
    return list_length


def isNotImg(url):
    reg = r'.+\.jpg|jpeg|gif|png|bmp|ico|mpg|mp4|css|js'
    hasReg = re.compile(reg)
    list_length = len(re.findall(hasReg, url))
    if list_length == 0:
        return True
    else:
        return False


def urlAborted(url):
    list = ['hdpreload', 'hao123', 'jdpay', 'weibo', 's9w','w3']
    for key in list:
        if url.find(key) != -1:
            return True
    return False


def getHtml(url):
    global response, html
    try:
        response = urllib.request.urlopen(url)  # open=urlopen response.getcode()
    except HTTPError as e:
        print('Error code:', e.code)
    except URLError as e:
        print('Reason', e.reason)
    except:
        print('Error unknown')
    if (response.getcode() == 200):
        try:
            html = response.read().decode('utf-8')
        except UnicodeDecodeError as e:
            print('Reason', e.reason)
    else:
        html = ""
    return html


# html = getHtml("http://www.baidu.com/baidu?wd=jd&tn=monline_dg&ie=utf-8")
print(findUrl("http://www.baidu.com/baidu?wd=jd&tn=monline_dg&ie=utf-8"))