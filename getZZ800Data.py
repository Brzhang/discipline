from pytdx.hq import TdxHq_API
import pandas
import xlrd
import requests
import os
import mysqlOp
import datetime
import constant

def isDataExist(dateName, table):
    conn = mysqlOp.connectMySQL()
    sql = 'select count(*) count from ' + table + ' where date="' + dateName + '"'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    if ret[0]['count'] > 0:
        return True
    else:
        return False

def downloadZZ800():
    print('will download zz800')
    zz800file = requests.get(constant.ZZ800fileUrl, headers = constant.ZZ800fileDownloadHeaders)
    open('./Data/' + constant.ZZ800fileName, 'wb').write(zz800file.content)
    return True

dtype={
      '成分券代码Constituent Code':str
      }  

def readZZ800Data(fileName):
    if os.path.exists('./Data/'+ fileName):
        try:
            content=xlrd.open_workbook(filename='./Data/'+ fileName,encoding_override='gb2312')
        except Exception as e:
            print('Error:',e, fileName + ' read failed')
            return None
        Data800 = pandas.read_excel(content, engine='xlrd', dtype=dtype, parse_dates=['日期Date'])
        if len(Data800) == 0:
            return None
        Data800.columns = ['date', 'index_code', 'index_name', 'index_name_en', 'code', 'name', 'name_en', 'jys', 'jys_en']
        Data800.drop(['index_code','index_name','index_name_en','name_en','jys','jys_en'],axis=1,inplace=True)
        return Data800
    else:
        #os.remove('./Data/'+ fileName)
        print(fileName + ' read failed')
        return None

def createZZ800Table():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'zz800list (data_id INT(11) AUTO_INCREMENT, code VARCHAR(45) DEFAULT NULL, name VARCHAR(45) DEFAULT NULL,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def creatLastStockPriceTable():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'last_stock_price (data_id INT(11) AUTO_INCREMENT, code VARCHAR(45) DEFAULT NULL,\
        close FLOAT DEFAULT 0.0, date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def creatStockTable(stockCode):
    conn = mysqlOp.connectMySQL()
    tbInfo = stockCode + ' (data_id INT AUTO_INCREMENT, code VARCHAR(45) DEFAULT NULL,\
        open FLOAT DEFAULT 0.0, close FLOAT DEFAULT 0.0, high FLOAT DEFAULT 0.0, low FLOAT DEFAULT 0.0,\
        vol FLOAT DEFAULT 0.0, amount FLOAT DEFAULT 0.0, date DATE,\
        PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def saveData(data, table):
    if data is None:
        return
    if isDataExist(data['date'][0].strftime('%Y%m%d'), table):
        return
    conn = mysqlOp.connectMySQL()
    data.to_sql(name=table, con = conn, if_exists='append', index=False)
    conn.close()

def saveStockData(table,data):
    if data is None:
        return
    if isDataExist(data['date'][0], table):
        return
    conn = mysqlOp.connectMySQL()
    data.to_sql(name=table, con = conn, if_exists='append', index=False)
    conn.close()

def getLastStockDate(stockCode):
    sql = 'select tb.date from ' + stockCode + ' tb order by tb.date DESC'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchOne(conn, sql)
    conn.close()
    return ret

def getStockData(api, stock):
    print('get socket data :', stock)
    creatStockTable('c' + stock)
    startDate = getLastStockDate('c' + stock)
    if startDate is None:
        startDate = constant.DataStartDate
    else:
        startDate = (startDate[0] + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    if startDate <= datetime.date.today().strftime('%Y-%m-%d'):
        data = api.get_k_data(stock, startDate, datetime.date.today().strftime('%Y-%m-%d'))
        if len(data) > 0:
            saveStockData('c'+ stock, data)
            updateStockPrice(stock, data['close'][-1], data['date'][-1])

def getStocksdata(stockCodelist):
    api = TdxHq_API()
    if api.connect(constant.HQServerIP, constant.HQServerPort):
        for stock in stockCodelist:
            getStockData(api, stock)
        api.disconnect()

def getLastDate():
    sql = 'select tb.date from zz800list tb order by tb.date DESC'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchOne(conn, sql)
    conn.close()
    return ret

def getZZ800CodeList(date):
    #if date == datetime.date.today().strftime('%Y-%m-%d'):
    date = getLastDate()[0].strftime('%Y%m%d')
    sql = 'select tb.code, tb.Name from zz800list tb where tb.date = "' + date + '"'
    conn = mysqlOp.connectMySQL()
    codes = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return codes

def getStockKData(stockCode, start, end):
    sql = 'select * from ' + stockCode + ' where date <= "' + end + '" and date >= "' + start + '"'
    conn = mysqlOp.connectMySQL()
    KData = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return KData

def getZZ800List():
    createZZ800Table()
    creatLastStockPriceTable()
    if not os.path.exists('./Data'):
        os.mkdir('./Data')
    if downloadZZ800():
        data = readZZ800Data(constant.ZZ800fileName)
        saveData(data, 'zz800list')
        getStocksdata(data['code'])
    print('get ZZ800 data completed. ' , datetime.datetime.now())

def updateStockPrice(code, price, date):
    sql = 'select * from last_stock_price where code = "' + code + '"'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchALL(conn, sql)
    if len(ret) > 0 :
        sql = 'update last_stock_price set close = ' + str(price) + ', date = "' + date+ '" where code = "' + code + '"'
    else:
        sql = 'insert into last_stock_price(code,close,date) values("' + code + '",' + str(price) + ',"' + date + '")'
    mysqlOp.executeSQL(conn, sql)
    conn.close()
