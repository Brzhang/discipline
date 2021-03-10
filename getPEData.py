import pandas
import xlrd
import requests
import zipfile
import datetime
import os
import mysqlOp
import drawLine
import constant

dtype={
        '行业代码':str,
        '行业名称':str,
        '证券代码':str,
        '四级行业代码':str
    }   

def filerData(data):
    data.drop(data[data['行业代码'].apply(lambda x: len(x)<8)].index, inplace=True)
    return data

def readPEData(fileName):
    if os.path.exists('./Data/tmp/'+ fileName):
        try:
            content=xlrd.open_workbook(filename='./Data/tmp/'+ fileName, encoding_override='gb2312')
        except Exception as e:
            print('Error:',e, fileName + ' read failed')
            return None
        dataPE = pandas.DataFrame(pandas.read_excel(content, engine='xlrd', sheet_name='中证行业滚动市盈率', dtype=dtype))
        dataPE = filerData(dataPE)
        if len(dataPE) == 0:
            return None
        dataPE.columns = ['HYCode', 'HYName', 'dynamicPE', 'stockNum', 'lostNum', 'PEAvgMonth', 'PEAvg3Month', 'PEAvg6Month', 'PEAvgYear']
        dataPE['dynamicPE'] = dataPE.apply(lambda x: float(x['dynamicPE']) if x['dynamicPE'] is not '-' else 0.0, axis=1)
        dataPE['stockNum'] = dataPE.apply(lambda x: int(x['stockNum']) if x['stockNum'] is not '-' else 0, axis=1)
        dataPE['lostNum'] = dataPE.apply(lambda x: int(x['lostNum']) if x['lostNum'] is not '-' else 0, axis=1)
        dataPE['PEAvgMonth'] = dataPE.apply(lambda x: float(x['PEAvgMonth']) if x['PEAvgMonth'] is not '-' else 0.0, axis=1)
        dataPE['PEAvg3Month'] = dataPE.apply(lambda x: float(x['PEAvg3Month']) if x['PEAvg3Month'] is not '-' else 0.0, axis=1)
        dataPE['PEAvg6Month'] = dataPE.apply(lambda x: float(x['PEAvg6Month']) if x['PEAvg6Month'] is not '-' else 0.0, axis=1)
        dataPE['PEAvgYear'] = dataPE.apply(lambda x: float(x['PEAvgYear']) if x['PEAvgYear'] is not '-' else 0.0, axis=1)
        return dataPE
    else:
        #os.remove('./Data/'+ fileName)
        print(fileName + ' read failed')
        return None

def readDYRData(fileName):
    if os.path.exists('./Data/tmp/'+ fileName):
        try:
            content=xlrd.open_workbook(filename='./Data/tmp/'+ fileName, encoding_override='gb2312')
        except Exception as e:
            print('Error:',e, fileName + ' read failed')
            return None
        dataDYR = pandas.DataFrame(pandas.read_excel(content, engine='xlrd', sheet_name='中证行业股息率', dtype=dtype))
        dataDYR = filerData(dataDYR)
        if len(dataDYR) == 0:
            return None
        dataDYR.columns = ['HYCode', 'HYName', 'DYR', 'stockNum', 'NoDYRNum', 'DYRAvgMonth', 'DYRAvg3Month', 'DYRAvg6Month', 'DYRAvgYear']
        dataDYR['DYR'] = dataDYR.apply(lambda x: float(x['DYR']) if x['DYR'] is not '-' else 0.0, axis=1)
        dataDYR['stockNum'] = dataDYR.apply(lambda x: int(x['stockNum']) if x['stockNum'] is not '-' else 0, axis=1)
        dataDYR['NoDYRNum'] = dataDYR.apply(lambda x: int(x['NoDYRNum']) if x['NoDYRNum'] is not '-' else 0, axis=1)
        dataDYR['DYRAvgMonth'] = dataDYR.apply(lambda x: float(x['DYRAvgMonth']) if x['DYRAvgMonth'] is not '-' else 0.0, axis=1)
        dataDYR['DYRAvg3Month'] = dataDYR.apply(lambda x: float(x['DYRAvg3Month']) if x['DYRAvg3Month'] is not '-' else 0.0, axis=1)
        dataDYR['DYRAvg6Month'] = dataDYR.apply(lambda x: float(x['DYRAvg6Month']) if x['DYRAvg6Month'] is not '-' else 0.0, axis=1)
        dataDYR['DYRAvgYear'] = dataDYR.apply(lambda x: float(x['DYRAvgYear']) if x['DYRAvgYear'] is not '-' else 0.0, axis=1)
        return dataDYR
    else:
        #os.remove('./Data/'+ fileName)
        print(fileName + ' read failed')
        return None

def readStockInfoData(fileName):
    if os.path.exists('./Data/tmp/'+ fileName):
        try:
            content=xlrd.open_workbook(filename='./Data/tmp/'+ fileName, encoding_override='gb2312')
        except Exception as e:
            print('Error:',e, fileName + ' read failed')
            return None
        dataStock = pandas.DataFrame(pandas.read_excel(content, engine='xlrd', sheet_name='个股数据', dtype=dtype))
        if len(dataStock) == 0:
            return None
        dataStock.columns = ['code', 'name', 'Level1HYCode', 'Level1HYName', 'Level2HYCode', 'Level2HYName', 'Level3HYCode', 'Level3HYName',
                             'Level4HYCode', 'Level4HYName', 'PE', 'DynamicPE', 'PB', 'DYR']
        dataStock.drop(['Level1HYCode', 'Level1HYName', 'Level2HYCode', 'Level2HYName', 'Level3HYCode', 'Level3HYName'], axis=1, inplace=True)
        dataStock['PE'] = dataStock.apply(lambda x: float(x['PE']) if x['PE'] is not '-' else 0.0, axis=1)
        dataStock['DynamicPE'] = dataStock.apply(lambda x: float(x['DynamicPE']) if x['DynamicPE'] is not '-' else 0.0, axis=1)
        dataStock['PB'] = dataStock.apply(lambda x: float(x['PB']) if x['PB'] is not '-' else 0.0, axis=1)
        dataStock['DYR'] = dataStock.apply(lambda x: float(x['DYR']) if x['DYR'] is not '-' else 0.0, axis=1)
        return dataStock
    else:
        #os.remove('./Data/'+ fileName)
        print(fileName + ' read failed')
        return None

def makePEFilePath(dateName):
    if not os.path.exists('./Data/' + dateName[0:4] + '/'):
        os.mkdir('./Data/' + dateName[0:4] + '/')
    if not os.path.exists('./Data/' + dateName[0:4] + '/' + dateName[4:6]+ '/'):
        os.mkdir('./Data/' + dateName[0:4] + '/' + dateName[4:6]+ '/')
    return './Data/' + dateName[0:4] + '/' + dateName[4:6]+ '/'

def unzip(fileWithPath):
    with zipfile.ZipFile(fileWithPath) as zf:
        zf.extractall('./Data/tmp/')

def downloadPEDataFile(fileName, dateName):
    if not os.path.exists(makePEFilePath(dateName) + fileName):
        url= constant.PEDataUrl + fileName
        downlaodfile = requests.get(url)
        if downlaodfile.status_code != 404:
            open(makePEFilePath(dateName) + fileName, 'wb').write(downlaodfile.content)
            unzip(makePEFilePath(dateName) + fileName)
            return True
        else:
            return False
    unzip(makePEFilePath(dateName) + fileName)
    return True

def createPETable():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'PEData (data_id INT(11) AUTO_INCREMENT, HYCode VARCHAR(45) DEFAULT NULL, HYName VARCHAR(45) DEFAULT NULL, \
        dynamicPE FLOAT DEFAULT 0.0, stockNum INT DEFAULT 0, lostNum INT DEFAULT 0, PEAvgMonth FLOAT DEFAULT 0.0,\
        PEAvg3Month FLOAT DEFAULT 0.0, PEAvg6Month FLOAT DEFAULT 0.0, PEAvgYear FLOAT DEFAULT 0.0,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def createDYRTable():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'DYRData (data_id INT(11) AUTO_INCREMENT, HYCode VARCHAR(45) DEFAULT NULL, HYName VARCHAR(45) DEFAULT NULL,\
        DYR FLOAT DEFAULT 0.0, stockNum INT DEFAULT 0, NoDYRNum INT DEFAULT 0, DYRAvgMonth FLOAT DEFAULT 0.0,\
        DYRAvg3Month FLOAT DEFAULT 0.0, DYRAvg6Month FLOAT DEFAULT 0.0, DYRAvgYear FLOAT DEFAULT 0.0,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def createStockInfo():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'stockInfo (data_id INT(11) AUTO_INCREMENT, code VARCHAR(45) DEFAULT NULL, name VARCHAR(45) DEFAULT NULL,\
        Level4HYcode VARCHAR(45) DEFAULT NULL, Level4HYname VARCHAR(80) DEFAULT NULL, PE FLOAT DEFAULT 0.0, DynamicPE FLOAT DEFAULT 0.0,\
        PB FLOAT DEFAULT 0.0, DYR FLOAT DEFAULT 0.0, date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def isDataExist(dateName, table):
    conn = mysqlOp.connectMySQL()
    sql = 'select count(*) count from ' + table + ' where date=' + dateName
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    if ret[0]['count'] > 0:
        return True
    else:
        return False

def saveData(data, dateName, table, type):
    if data is None:
        return
    conn = mysqlOp.connectMySQL()
    data['date'] = datetime.datetime.strptime(dateName, '%Y%m%d')
    data.to_sql(name=table, con = conn, if_exists='append', index=False)
    conn.close()

def getHYTypeFromDB(table):
    conn = mysqlOp.connectMySQL()
    sql = 'select tb.HYCode from ' + table + ' tb where tb.date > "'+ constant.DataStartDate +'" group by tb.HYCode'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def getHYDataFromDB(table, HYCode):
    conn = mysqlOp.connectMySQL()
    sql = 'select * from ' + table + ' where HYCode=' + HYCode + ' and date > "' + constant.DataStartDate + '"'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def drewPEDateLines():
    if not os.path.exists('./Data/Pics'):
        os.mkdir('./Data/Pics')
    HYCodes = getHYTypeFromDB('PEData')
    for code in HYCodes:
        data = getHYDataFromDB('PEData', code['HYCode'])
        lineNames = ['dynamicPE', 'MonthAvg', '3MonthAvg', '6MonthAvg','YearAvg']
        df = pandas.DataFrame(data)
        df.columns = data[0].keys()
        Ys = [df['dynamicPE'], df['PEAvgMonth'], df['PEAvg3Month'], df['PEAvg6Month'], df['PEAvgYear']]
        colors = ['red','blue','green','yellow','black']
        drawLine.drawLines(df['date'], Ys, lineNames, colors ,'PE-'+ code['HYCode'], './Data/Pics/' + df['HYName'][0])

def getLastDate():
    sql = 'select tb.date from PEData tb order by tb.date DESC'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchOne(conn, sql)
    conn.close()
    return ret

def getStockInfoWithCode(stockCode):
    sql = 'select * from stockInfo where code=' + stockCode
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def getPEData():
    createPETable()
    createDYRTable()
    createStockInfo()
    if not os.path.exists('./Data'):
        os.mkdir('./Data')
    if not os.path.exists('./Data/tmp/'):
        os.mkdir('./Data/tmp/')
    endDate = datetime.date.today()
    '''startDate is the lastest date read form db . if is none it's the date five years ago'''
    startDate = getLastDate()
    if startDate is None:
        startDate = datetime.datetime.strptime(constant.DataStartDate, '%Y-%m-%d %H:%M:%S')
    else:
        startDate = startDate[0]
    print(startDate)
    for i in range((endDate - startDate).days + 1):
        dateName = (startDate + datetime.timedelta(days=i)).strftime('%Y%m%d')
        if isDataExist(dateName, 'PEData') and isDataExist(dateName, 'DYRData'):
            continue
        fileName = 'csi' + dateName + '.zip'
        if downloadPEDataFile(fileName, dateName):
            fileName = 'csi' + dateName + '.xls'
            saveData(readPEData(fileName), dateName, 'PEData', 'append')
            saveData(readDYRData(fileName), dateName, 'DYRData', 'append')
            if(dateName == endDate.strftime('%Y%m%d')):
                saveData(readStockInfoData(fileName), dateName, 'stockInfo', 'replace')
            if os.path.exists('./Data/tmp/'+fileName):
                os.remove('./Data/tmp/'+fileName)