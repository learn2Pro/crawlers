from kafka import KafkaProducer
from kafka.errors import KafkaError
import log
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
    global i
    i += 1
    producer = KafkaProducer(bootstrap_servers=['master:9092', 'slave:9092'])
    key = 'logs-' + str(i)
    producer.send('htmls', key=str.encode(key, encoding='utf-8'), value=str.encode(html, encoding='utf-8'))
    producer.close(timeout=10)
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
                except Exception as e:
                    print("cannot add to x!", e)
    return x


i = 0
print(findUrl("https://www.google.com.hk/search?q=jd&rlz=1C1CHWL_zh-cnUS724US724&oq=jd&aqs=chrome..69i57j69i60l4j69i59.311j0j8&sourceid=chrome&ie=UTF-8"))
# print(findUrl("http://www.baidu.com/baidu?wd=jd&tn=monline_dg&ie=utf-8"))

# Asynchronous by default
# future = producer.send('test-logs', b'raw_bytes')
#
# # Block for 'synchronous' sends
# try:
#     record_metadata = future.get(timeout=1000)
# except KafkaError:
#     # Decide what to do if produce request failed...
#     log.exception()
#     pass
#
# # Successful result returns assigned partition and offset
# print(record_metadata.topic)
# print(record_metadata.partition)
# print(record_metadata.offset)
#
# # produce keyed messages to enable hashed partitioning
# for _ in range(105):
#     producer.send('test-logs', key=b'foo4', value=b'bar4')


# # encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps)
# producer.send('msgpack-topic', {'key': 'value'})
#
# # produce json messages
# producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
# producer.send('json-topic', {'key': 'value'})
#
# # produce asynchronously
# for _ in range(100):
#     producer.send('test-logs', b'msg')

# block until all async messages are sent
# producer.flush()

# configure multiple retries
# producer = KafkaProducer(retries=5)
