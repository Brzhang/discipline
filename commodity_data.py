import os
import urllib.request
import requests
import pandas
import json
import mysqlOp
import datetime
import constant
import drawLine

pandas.set_option('display.width', 300) # 设置字符显示宽度
pandas.set_option('display.max_rows', None) # 设置显示最大行
pandas.set_option('display.max_columns', None) # 设置显示最大列，None为显示所有列

class CommodityBase:
    url = ''
    request_header = {}
    table_name = ''
    
    def __init__(self, url, request_header, table_name):
        self.url = url
        self.request_header = request_header
        self.table_name = table_name
        self.createTable()
        
    def createTable(self):
        conn = mysqlOp.connectMySQL()
        tbInfo = self.table_name + ' (data_id INT(11) AUTO_INCREMENT, contract_name VARCHAR(45) DEFAULT NULL, member_type VARCHAR(45) DEFAULT NULL,\
            total_vol INT DEFAULT 0, delta_vol INT DEFAULT 0,\
            buy_vol INT DEFAULT 0, delta_buy INT DEFAULT 0, sell_vol INT DEFAULT 0, delta_sell INT DEFAULT 0,\
            date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
        mysqlOp.createTable(conn, tbInfo)
        conn.close()
    def getLastDate(self):
        sql = 'select tb.date from ' + self.table_name + ' tb order by tb.date DESC'
        conn = mysqlOp.connectMySQL()
        ret = mysqlOp.fetchOne(conn, sql)
        conn.close()
        return ret
    def isDataExist(self, dateName):
        conn = mysqlOp.connectMySQL()
        sql = 'select count(*) count from ' + self.table_name + ' where date="' + dateName + '"'
        ret = mysqlOp.fetchALL(conn, sql)
        conn.close()
        if ret[0]['count'] > 0:
            return True
        else:
            return False
    def saveToDB(self, data):
        if data is None:
            return
        conn = mysqlOp.connectMySQL()
        data.to_sql(name=self.table_name, con = conn, if_exists='append', index=False)
        conn.close()
    def getData(self):
        endDate = datetime.date.today()
        startDate = self.getLastDate()
        if startDate is None:
            startDate = endDate + datetime.timedelta(days=-90)
        else:
            startDate = startDate[0]
        print('start date: ', startDate, ' endDate: ', endDate)
        for i in range((endDate - startDate).days + 1):
            dateName = startDate + datetime.timedelta(days=i)
            if self.isDataExist(dateName.strftime('%Y-%m-%d')):
                continue
            self.getPeerDayData(dateName)
    def getDataFromDB(self, contract_name):
        sql = 'select * from ' + self.table_name + ' where contract_name = "' + contract_name + '"'
        conn = mysqlOp.connectMySQL()
        data = mysqlOp.fetchALL(conn, sql)
        conn.close()
        data = pandas.DataFrame(data)
        data.columns = ['data_id', 'contract_name', 'member_type', 'total_vol', 'delta_vol', 'buy_vol', 'delta_buy', 'sell_vol', 'delta_sell', 'date']
        return data
    def mkRequestParam(self, date):
        request_param = {} 
        return request_param
    def getContractName(self):
        sql = 'select tb.contract_name from ' + self.table_name + ' tb group by tb.contract_name'
        conn = mysqlOp.connectMySQL()
        ret = mysqlOp.fetchALL(conn, sql)
        conn.close()
        datalist = []
        for contract_name in ret:
            datalist.append(contract_name[0].strip())
        return datalist
    def getPeerDayData(self, date):
        return
    def draw(self, data, picname):
        lineNames = ['buy', 'sell']
        #print(data)
        Ys = [data['buy_vol'].tolist(), data['sell_vol'][:].tolist()]
        colors = ['#5470c6','#91cc75']
        drawLine.drawLines(data['date'], Ys, lineNames, colors , picname, './Data/Pics/' + picname).close()

class CommodityDCE(CommodityBase):
    url = 'http://www.dce.com.cn/publicweb/quotesdata/memberDealPosiQuotes.html'
    request_header = {'Content-Type': 'application/x-www-form-urlencoded; charset:UTF-8'}
    contract_name = ''
    def __init__(self, table_name, contract_name):
        self.contract_name = contract_name
        super(CommodityDCE, self).__init__(self.url, self.request_header, table_name)
    def getPeerDayData(self, date):
        request_param = self.mkRequestParam(date)
        print(request_param)
        request_param = bytes(urllib.parse.urlencode(request_param),encoding='utf-8')
        request = urllib.request.Request(url=self.url, data=request_param, headers=self.request_header, method='POST')
        data_text = urllib.request.urlopen(request).read()
        try:
            tbl = pandas.read_html(data_text, encoding='utf-8')
            tbl = pandas.DataFrame(tbl[0])
            # 会员类别	总成交量	增减	总持买单量	增减	总持卖单量	增减
            tbl.columns = ['member_type', 'total_vol', 'delta_vol', 'buy_vol', 'delta_buy', 'sell_vol', 'delta_sell']
            tbl['contract_name'] = self.contract_name
            tbl['date'] = date
            print(tbl)
            self.saveToDB(tbl)
        except ValueError:
            pass
    def getLastDate(self):
        sql = 'select tb.date from ' + self.table_name + ' tb where contract_name="' + self.contract_name +'" order by tb.date DESC'
        conn = mysqlOp.connectMySQL()
        ret = mysqlOp.fetchOne(conn, sql)
        conn.close()
        return ret
    def isDataExist(self, dateName):
        conn = mysqlOp.connectMySQL()
        sql = 'select count(*) count from ' + self.table_name + ' where date="' + dateName + '" and contract_name="' + self.contract_name + '"'
        ret = mysqlOp.fetchALL(conn, sql)
        conn.close()
        if ret[0]['count'] > 0:
            return True
        else:
            return False
    def getDataFromDB(self):
        return super(CommodityDCE, self).getDataFromDB(self.contract_name)
    def draw(self, data):
        return super(CommodityDCE, self).draw(data, self.contract_name)

class CommoditySHFE(CommodityBase):
    url = 'http://www.shfe.com.cn/data/dailydata/kx/pm' #20210803.dat
    request_header = {'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Host': 'www.shfe.com.cn',
                    'Referer': 'http://www.shfe.com.cn/statements/dataview.html?paramid=pm',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}
    contract_kind = ''
    def __init__(self, table_name, contract_kind):
        self.contract_kind = contract_kind
        self.createDailyDataTable()
        super(CommoditySHFE, self).__init__(self.url, self.request_header, table_name)
    def getPeerDayData(self, date):
        datas = self.getDailyData(date.strftime('%Y-%m-%d'))
        data_text = None
        if len(datas) == 0:
            request = urllib.request.Request(url=self.url + date.strftime('%Y%m%d')+'.dat', headers=self.request_header, method='GET')
            try:
                data_text = urllib.request.urlopen(request)
                data_text = data_text.read().decode('utf-8')
                self.saveDailyData(data_text, date.strftime('%Y-%m-%d'))
            except urllib.error.HTTPError:
                pass
        else:
            data_text = datas[0][0]
        if data_text is not None:
            #print(data_text)
            data_json = json.loads(data_text)
            data_list: List[Any] = []
            for item in data_json['o_cursor']:# 记录所有合约的合约总计
                if self.contract_kind in item['INSTRUMENTID'] and item['RANK'] == 999:
                    data_list.append(item)
            data_df = pandas.DataFrame(data_list)
            #{"INSTRUMENTID":"cu2110","PRODUCTSORTNO":100,"RANK":999,"PARTICIPANTID1":"","PARTICIPANTABBR1":"","CJ1":391,"CJ1_CHG":58,"PARTICIPANTID2":"","PARTICIPANTABBR2":"","CJ2":503,"CJ2_CHG":-4,"PARTICIPANTID3":"","PARTICIPANTABBR3":"","CJ3":491,"CJ3_CHG":0,"PRODUCTNAME":""}
            # 会员类别	总成交量	增减	总持买单量	增减	总持卖单量	增减
            data_df.columns = ['contract_name','productsortno','rank','member_type','participantabbr1','total_vol', 'delta_vol','participantid2','participantabbr2', 'buy_vol', 'delta_buy','participantid3','participantabbr3', 'sell_vol', 'delta_sell','productname']
            data_df.drop(['productsortno', 'rank', 'participantabbr1', 'participantid2', 'participantabbr2', 'participantid3', 'participantabbr3','productname'], axis=1, inplace=True)
            data_df['date'] = date
            data_df['member_type'] = '期货公司会员'
            data_df['contract_name'] = data_df.apply(lambda x: x['contract_name'].strip(), axis=1)
            data_df['total_vol'] = data_df.apply(lambda x: x['total_vol'] if x['total_vol'] != '' else 0, axis=1)
            data_df['delta_vol'] = data_df.apply(lambda x: x['delta_vol'] if x['delta_vol'] != '' else 0, axis=1)
            #print(data_df)
            self.saveToDB(data_df)

    def saveDailyData(self, data, date):
        if data is None:
            return
        sql = 'insert into shfe_daily(context,date) values("' + mysqlOp.escapeString(data) + '","' + date + '")'
        conn = mysqlOp.connectMySQL()
        mysqlOp.executeSQL(conn,sql)

    def getDailyData(self, date):
        sql = 'select context from shfe_daily where date = "' + date + '"'
        conn = mysqlOp.connectMySQL()
        ret = mysqlOp.fetchALL(conn, sql)
        conn.close()
        return ret

    def createDailyDataTable(self):
        conn = mysqlOp.connectMySQL()
        tbInfo = 'shfe_daily (data_id INT(11) AUTO_INCREMENT, context LONGTEXT DEFAULT NULL, date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
        mysqlOp.createTable(conn, tbInfo)
        conn.close()

    def getDataFromDB(self, contract_name):
        return super(CommoditySHFE, self).getDataFromDB(contract_name)

    def draw(self, data, contract_name):
        return super(CommoditySHFE, self).draw(data, contract_name)

class CommodityCFFEX(CommodityBase):
    url = 'http://www.cffex.com.cn/sj/ccpm/' #202108/03/IC_1.csv'
    request_header = {'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                    'Host': 'www.cffex.com.cn',
                    'Referer': 'http://www.cffex.com.cn/ccpm/',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55'}
    contract_name = ''
    def __init__(self, table_name, contract_name):
        self.contract_name = contract_name
        super(CommodityCFFEX, self).__init__(self.url, self.request_header, table_name)
    def getPeerDayData(self, date):
        filepath = self.makeDownloadFilePath() + date.strftime('%Y%m%d') + '.csv'
        if not os.path.exists(filepath):
            fileurl = self.url + date.strftime('%Y%m/%d') + '/' + self.contract_name + '_1.csv'
            downlaodfile = requests.get(fileurl)
            if '<title>网页错误</title>' not in downlaodfile.content.decode('gb2312'):
                open(filepath , 'wb').write(downlaodfile.content)
            else:
                return
        data = self.readFile(filepath)
        data.drop(0, inplace=True)
        data.columns = ['date', 'contract_name', 'sort', 'member_type', 'total_vol', 'delta_vol', 'member_type1', 'buy_vol', 'delta_buy', 'member_type2', 'sell_vol', 'delta_sell']
        data.drop(['date','sort', 'member_type', 'member_type1' , 'member_type2'], axis=1, inplace=True)
        data['total_vol'] = data.apply(lambda x: int(x['total_vol']), axis=1)
        data['delta_vol'] = data.apply(lambda x: int(x['delta_vol']), axis=1)
        data['buy_vol'] = data.apply(lambda x: int(x['buy_vol']), axis=1)
        data['delta_buy'] = data.apply(lambda x: int(x['delta_buy']), axis=1)
        data['sell_vol'] = data.apply(lambda x: int(x['sell_vol']), axis=1)
        data['delta_sell'] = data.apply(lambda x: int(x['delta_sell']), axis=1)
        data = data.groupby('contract_name').sum()
        data['date'] = date
        data['member_type'] = '期货公司会员'
        data.reset_index(['contract_name'], inplace=True)
        self.saveToDB(data)
        
    def makeDownloadFilePath(self):
        filepath = './Data/' + self.contract_name + '/'
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        return filepath

    def readFile(self, filepath):
        if os.path.exists(filepath):
            data = pandas.read_csv(filepath, encoding='gb2312')
            return data
        else:
            #os.remove('./Data/'+ fileName)
            print(filepath + ' read failed')
            return None

    def getDataFromDB(self, contract_name):
        return super(CommodityCFFEX, self).getDataFromDB(contract_name)

    def draw(self, data, contract_name):
        return super(CommodityCFFEX, self).draw(data, contract_name)


class CoinData(CommodityDCE):
    def __init__(self, contract_name):
        super(CoinData, self).__init__('coin_data', 'c' + contract_name)

    def mkRequestParam(self, date):
        request_param = {'memberDealPosiQuotes.variety': 'c',
                        'memberDealPosiQuotes.trade_type': '0',
                        'year': str(date.year),
                        'month': str(date.month-1),
                        'day': str(date.day),
                        'contract.contract_id': self.contract_name,
                        'contract.variety_id': 'c',
                        'contract':''} 
        return request_param

class PorkData(CommodityDCE):
    def __init__(self, contract_name):
        super(PorkData, self).__init__('pork_data', 'lh' + contract_name)

    def mkRequestParam(self, date):
        request_param = {'memberDealPosiQuotes.variety': 'lh',
                        'memberDealPosiQuotes.trade_type': '0',
                        'year': str(date.year),
                        'month': str(date.month-1),
                        'day': str(date.day),
                        'contract.contract_id': self.contract_name,
                        'contract.variety_id': 'lh',
                        'contract':''} 
        return request_param

class CuData(CommoditySHFE):
    def __init__(self):
        super(CuData, self).__init__('cu_data', 'cu')

class AuData(CommoditySHFE):
    def __init__(self):
        super(AuData, self).__init__('au_data', 'au')

class RuData(CommoditySHFE):
    def __init__(self):
        super(RuData, self).__init__('ru_data', 'ru')

class ICData(CommodityCFFEX):
    def __init__(self):
        super(ICData, self).__init__('ic_data', 'IC')
class IHData(CommodityCFFEX):
    def __init__(self):
        super(IHData, self).__init__('ih_data', 'IH')

if __name__=='__main__':
    coin = CoinData('2201')
    coin.getData()
    coin.draw(coin.getDataFromDB())
    pork = PorkData('2201')
    pork.getData()
    pork.draw(pork.getDataFromDB())

    cu = CuData()
    cu.getData()
    contractlist = cu.getContractName()
    for name in contractlist:
        cu.draw(cu.getDataFromDB(name),name)

    au = AuData()
    au.getData()
    contractlist = au.getContractName()
    for name in contractlist:
        au.draw(au.getDataFromDB(name),name)

    ru = RuData()
    ru.getData()
    contractlist = ru.getContractName()
    for name in contractlist:
        ru.draw(ru.getDataFromDB(name),name)

    ic = ICData()
    ic.getData()
    contractlist = ic.getContractName()
    for name in contractlist:
        ic.draw(ic.getDataFromDB(name),name)

    ih = IHData()
    ih.getData()
    contractlist = ih.getContractName()
    for name in contractlist:
        ih.draw(ih.getDataFromDB(name),name)