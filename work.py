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
                    print("cannot add to x!")
    return x


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
    list = ['hdpreload', 'hao123', 'facebook', 'weibo', 's9w', 'w3', 'jd', 'joybuy', 'kela']
    for key in list:
        if url.find(key) != -1:
            return True
    return False


def getHtml(url):
    global response, html
    try:
        request = urllib.request.Request(url)  # open=urlopen response.getcode() header=response.info()
        request.add_header('Content-Type', 'text/html; charset=utf-8')
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0')
        response = urllib.request.urlopen(request, timeout=5)
    except HTTPError as e:
        print('Error code:', e.code)
    except URLError as e:
        print('Reason', e.reason)
    except:
        print('Error unknown')
    if (response.getcode() == 200):
        try:
            reg = r'charset=(.*)'
            hasReg = re.compile(reg)
            code = re.findall(hasReg, response.headers['Content-Type'])
            html = response.read().decode(code[0])
        except UnicodeDecodeError as e:
            print('Reason', e.reason)
    else:
        html = ""
    return html


# html = getHtml("http://www.baidu.com/baidu?wd=jd&tn=monline_dg&ie=utf-8")
print(findUrl("http://www.baidu.com/baidu?wd=jd&tn=monline_dg&ie=utf-8"))
# print(findUrl("http://list.tmall.com/search_product.htm?q=jd.com&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton"))
