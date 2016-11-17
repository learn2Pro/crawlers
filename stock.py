import urllib.request

debug = False


class Utility:
    def ToGB(str):
        if (debug): print(str)
        return str.decode('gb2312')


class StockInfo:
    """get stock information"""

    def GetStockStrByNum(num):
        f = urllib.request.urlopen('http://hq.sinajs.cn/list=' + str(num))
        if (debug): print(f.geturl())
        if (debug): print(f.info())
        return f.read()
        f.close()

    def ParseResultStr(resultstr):
        if (debug): print(resultstr)
        slist = resultstr.split(',')
        name = slist[0][-4:]
        yesterdayendprice = slist[2]
        todaystartprice = slist[1]
        nowprice = slist[3]
        upgraderate = (float(nowprice) - float(yesterdayendprice)) / float(yesterdayendprice)
        upgraderate = upgraderate * 100
        dateandtime = slist[30] + ' ' + slist[31]
        print('*******************************')
        print('name is :', name)
        print('yesterday end price is :', yesterdayendprice)
        print('today start price is :', todaystartprice)
        print('now price is :', nowprice)
        print('upgrade rate is :', upgraderate, '%')
        print('date and time is :', dateandtime)
        print('*******************************')

    def GetStockInfo(num):
        str = StockInfo.GetStockStrByNum(num)
        strGB = Utility.ToGB(str)
        StockInfo.ParseResultStr(strGB)


def Main():
    stocks = ['sz000988', 'sh600839', 'sh000001']
    for stock in stocks:
        StockInfo.GetStockInfo(stock)


Main()
