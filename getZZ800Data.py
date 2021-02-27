from pytdx.hq import TdxHq_API
import pandas
import xlrd
import requests
import os
import mysqlOp
import datetime

fileName = '000906cons.xls'

def isDataExist(dateName, table):
    conn = mysqlOp.connectMySQL()
    sql = 'select count(*) count from ' + table + ' where date=' + dateName.strftime("%Y%m-%d %H:%M:%S")
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    if ret[0]['count'] > 0:
        return True
    else:
        return False

def downloadZZ800():
    url='http://www.csindex.com.cn/uploads/file/autofile/cons/' + fileName
    zz800file = requests.get(url)
    open('./Data/' + fileName, 'wb').write(zz800file.content)
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
        Data800.columns = ['date', 'index_code', 'index_name', 'index_name_en', 'Code', 'Name', 'Name_en', 'jsy']
        Data800.drop(['index_code'],axis=1,inplace=True)
        Data800.drop(['index_name'],axis=1,inplace=True)
        Data800.drop(['index_name_en'],axis=1,inplace=True)
        Data800.drop(['Name_en'],axis=1,inplace=True)
        Data800.drop(['jsy'],axis=1,inplace=True)
        return Data800
    else:
        #os.remove('./Data/'+ fileName)
        print(fileName + ' read failed')
        return None

def createZZ800Table():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'ZZ800List (data_id INT(11) AUTO_INCREMENT, Code VARCHAR(45) DEFAULT NULL, Name VARCHAR(45) DEFAULT NULL,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def saveData(data, table):
    if data is None:
        return
    if isDataExist(data['date'][0], table):
        return
    conn = mysqlOp.connectMySQL()
    data.to_sql(name=table, con = conn, if_exists='append', index=False)
    conn.close()

def getStockdata(stocklist):
    api = TdxHq_API()
    with api.connect('119.147.212.81', 7709):
        for stock in stocklist:
            data = api.get_security_bars(9, 0, stocklist, 0, 10) #返回普通list
        return data
        #data = api.to_df(api.get_security_bars(9, 0, '000001', 0, 10)) # 返回DataFrame


def getLastDate():
    sql = 'select tb.date from ZZ800List tb order by tb.date DESC'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchOne(conn, sql)
    conn.close()
    return ret

def getZZ800List():
    createZZ800Table()
    if not os.path.exists('./Data'):
        os.mkdir('./Data')
    if downloadZZ800():
        saveData(readZZ800Data(fileName), 'ZZ800List')