import re
import urllib.request
from urllib.error import URLError, HTTPError
import urllib.parse


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
                    urlFile = open("/usr/local/works/data/urls", 'a')
                    urlFile.write(url + r'  ' + toUrl + '\n')
                    urlFile.close()
                    x += findUrl(toUrl)
                except Exception as e:
                    print("cannot add to x!", e)
    return x


# print(findUrl("https://www.google.com.hk/search?q=jd&rlz=1C1CHWL_zh-cnUS724US724&oq=jd&aqs=chrome..69i57j69i60l4j69i59.311j0j8&sourceid=chrome&ie=UTF-8"))
print(findUrl("http://www.baidu.com/baidu?wd=jd&tn=monline_dg&ie=utf-8"))
