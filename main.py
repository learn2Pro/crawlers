#####coding=utf-8

import re
import urllib.request

def getHtml(url):
    page = urllib.request.urlopen(url)
   ## print(type(page.info()))
   ## print(page.info())
    for i in range(0, 5):
        print(i)
    else:
        pass
    reg = r'charset=(\w+-\d+)\n'
    print(reg)
    imgre = re.compile(reg)
    imglist = re.findall(imgre, "Content-Type: text/html; charset=UTF-8\n")
    print(imglist)
 ##   print(page.getcode())
    html = page.read().decode('utf-8')
    return html


def getImg(html):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    x = 0
    for imgurl in imglist:
        urllib.request.urlretrieve(imgurl, '%s.jpg' % x)
        x += 1


html = getHtml("http://tieba.baidu.com/p/2460150866")
# print(html)
# getImg(html)
