import pandas
import xlrd
import requests
import zipfile
import datetime
from dateutil.relativedelta import relativedelta
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

calcedIndustryPE = {'time': datetime.datetime.now(), 'data': []}

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
        dataPE.columns = ['hy_code', 'hy_name', 'dynamic_pe', 'stocknum', 'lostnum', 'pe_avg_month', 'pe_avg_3month', 'pe_avg_6month', 'pe_avg_year']
        dataPE['dynamic_pe'] = dataPE.apply(lambda x: float(x['dynamic_pe']) if x['dynamic_pe'] != '-' else 0.0, axis=1)
        dataPE['stocknum'] = dataPE.apply(lambda x: int(x['stocknum']) if x['stocknum'] != '-' else 0, axis=1)
        dataPE['lostnum'] = dataPE.apply(lambda x: int(x['lostnum']) if x['lostnum'] != '-' else 0, axis=1)
        dataPE['pe_avg_month'] = dataPE.apply(lambda x: float(x['pe_avg_month']) if x['pe_avg_month'] != '-' else 0.0, axis=1)
        dataPE['pe_avg_3month'] = dataPE.apply(lambda x: float(x['pe_avg_3month']) if x['pe_avg_3month'] != '-' else 0.0, axis=1)
        dataPE['pe_avg_6month'] = dataPE.apply(lambda x: float(x['pe_avg_6month']) if x['pe_avg_6month'] != '-' else 0.0, axis=1)
        dataPE['pe_avg_year'] = dataPE.apply(lambda x: float(x['pe_avg_year']) if x['pe_avg_year'] != '-' else 0.0, axis=1)
        return dataPE
    else:
        #os.remove('./Data/'+ fileName)
        print(fileName + ' read failed')
        return None

def readPBData(fileName):
    if os.path.exists('./Data/tmp/'+ fileName):
        try:
            content=xlrd.open_workbook(filename='./Data/tmp/'+ fileName, encoding_override='gb2312')
        except Exception as e:
            print('Error:',e, fileName + ' read failed')
            return None
        dataPB = pandas.DataFrame(pandas.read_excel(content, engine='xlrd', sheet_name='中证行业市净率', dtype=dtype))
        dataPB = filerData(dataPB)
        if len(dataPB) == 0:
            return None
        dataPB.columns = ['hy_code', 'hy_name', 'pb', 'stocknum', 'lostnum', 'pb_avg_month', 'pb_avg_3month', 'pb_avg_6month', 'pb_avg_year']
        dataPB['pb'] = dataPB.apply(lambda x: float(x['pb']) if x['pb'] != '-' else 0.0, axis=1)
        dataPB['stocknum'] = dataPB.apply(lambda x: int(x['stocknum']) if x['stocknum'] != '-' else 0, axis=1)
        dataPB['lostnum'] = dataPB.apply(lambda x: int(x['lostnum']) if x['lostnum'] != '-' else 0, axis=1)
        dataPB['pb_avg_month'] = dataPB.apply(lambda x: float(x['pb_avg_month']) if x['pb_avg_month'] != '-' else 0.0, axis=1)
        dataPB['pb_avg_3month'] = dataPB.apply(lambda x: float(x['pb_avg_3month']) if x['pb_avg_3month'] != '-' else 0.0, axis=1)
        dataPB['pb_avg_6month'] = dataPB.apply(lambda x: float(x['pb_avg_6month']) if x['pb_avg_6month'] != '-' else 0.0, axis=1)
        dataPB['pb_avg_year'] = dataPB.apply(lambda x: float(x['pb_avg_year']) if x['pb_avg_year'] != '-' else 0.0, axis=1)
        return dataPB
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
        dataDYR.columns = ['hy_code', 'hy_name', 'dyr', 'stocknum', 'no_dyr_num', 'dyr_avg_month', 'dyr_avg_3month', 'dyr_avg_6month', 'dyr_avg_year']
        dataDYR['dyr'] = dataDYR.apply(lambda x: float(x['dyr']) if x['dyr'] != '-' else 0.0, axis=1)
        dataDYR['stocknum'] = dataDYR.apply(lambda x: int(x['stocknum']) if x['stocknum'] != '-' else 0, axis=1)
        dataDYR['no_dyr_num'] = dataDYR.apply(lambda x: int(x['no_dyr_num']) if x['no_dyr_num'] != '-' else 0, axis=1)
        dataDYR['dyr_avg_month'] = dataDYR.apply(lambda x: float(x['dyr_avg_month']) if x['dyr_avg_month'] != '-' else 0.0, axis=1)
        dataDYR['dyr_avg_3month'] = dataDYR.apply(lambda x: float(x['dyr_avg_3month']) if x['dyr_avg_3month'] != '-' else 0.0, axis=1)
        dataDYR['dyr_avg_6month'] = dataDYR.apply(lambda x: float(x['dyr_avg_6month']) if x['dyr_avg_6month'] != '-' else 0.0, axis=1)
        dataDYR['dyr_avg_year'] = dataDYR.apply(lambda x: float(x['dyr_avg_year']) if x['dyr_avg_year'] != '-' else 0.0, axis=1)
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
        dataStock.columns = ['code', 'name', 'level1_hy_code', 'level1_hy_name', 'level2_hy_code', 'level2_hy_name', 'level3_hy_code', 'level3_hy_name',
                             'level4_hy_code', 'level4_hy_name', 'pe', 'dynamic_pe', 'pb', 'dyr']
        dataStock.drop(['level1_hy_code', 'level1_hy_name', 'level2_hy_code', 'level2_hy_name', 'level3_hy_code', 'level3_hy_name'], axis=1, inplace=True)
        dataStock['dyr'] = dataStock.apply(lambda x: float(x['dyr']) if x['dyr'] != '-' else 0.0, axis=1)
        dataStock['pe'] = dataStock.apply(lambda x: float(x['pe']) if x['pe'] != '-' else 0.0, axis=1)
        dataStock['dynamic_pe'] = dataStock.apply(lambda x: float(x['dynamic_pe']) if x['dynamic_pe'] != '-' else 0.0, axis=1)
        dataStock['pb'] = dataStock.apply(lambda x: float(x['pb']) if x['pb'] != '-' else 0.0, axis=1)
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
        print('will download file:', fileName)
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
    tbInfo = 'pe_data (data_id INT(11) AUTO_INCREMENT, hy_code VARCHAR(45) DEFAULT NULL, hy_name VARCHAR(45) DEFAULT NULL, \
        dynamic_pe FLOAT DEFAULT 0.0, stocknum INT DEFAULT 0, lostnum INT DEFAULT 0, pe_avg_month FLOAT DEFAULT 0.0,\
        pe_avg_3month FLOAT DEFAULT 0.0, pe_avg_6month FLOAT DEFAULT 0.0, pe_avg_year FLOAT DEFAULT 0.0,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def createPBTable():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'pb_data (data_id INT(11) AUTO_INCREMENT, hy_code VARCHAR(45) DEFAULT NULL, hy_name VARCHAR(45) DEFAULT NULL, \
        pb FLOAT DEFAULT 0.0, stocknum INT DEFAULT 0, lostnum INT DEFAULT 0, pb_avg_month FLOAT DEFAULT 0.0,\
        pb_avg_3month FLOAT DEFAULT 0.0, pb_avg_6month FLOAT DEFAULT 0.0, pb_avg_year FLOAT DEFAULT 0.0,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def createDYRTable():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'dyr_data (data_id INT(11) AUTO_INCREMENT, hy_code VARCHAR(45) DEFAULT NULL, hy_name VARCHAR(45) DEFAULT NULL,\
        dyr FLOAT DEFAULT 0.0, stocknum INT DEFAULT 0, no_dyr_num INT DEFAULT 0, dyr_avg_month FLOAT DEFAULT 0.0,\
        dyr_avg_3month FLOAT DEFAULT 0.0, dyr_avg_6month FLOAT DEFAULT 0.0, dyr_avg_year FLOAT DEFAULT 0.0,\
        date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def createStockInfo():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'stock_info (data_id INT(11) AUTO_INCREMENT, code VARCHAR(45) DEFAULT NULL, name VARCHAR(45) DEFAULT NULL,\
        level4_hy_code VARCHAR(45) DEFAULT NULL, level4_hy_name VARCHAR(80) DEFAULT NULL, pe FLOAT DEFAULT 0.0, dynamic_pe FLOAT DEFAULT 0.0,\
        pb FLOAT DEFAULT 0.0, dyr FLOAT DEFAULT 0.0, date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
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
    if type == 'replace':
        type = 'append'
        sql = "delete from " + table + ' where data_id > 0'
        mysqlOp.executeSQL(conn, sql)
    data['date'] = datetime.datetime.strptime(dateName, '%Y%m%d').date()
    data.to_sql(name=table, con = conn, if_exists=type, index=False)
    conn.close()

def getHYTypeFromDB(table):
    conn = mysqlOp.connectMySQL()
    sql = 'select tb.hy_code from ' + table + ' tb where tb.date > "'+ constant.DataStartDate +'" group by tb.hy_code'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def getHYDataFromDB(table, HYCode):
    conn = mysqlOp.connectMySQL()
    sql = 'select * from ' + table + ' where hy_code=' + HYCode + ' and date > "' + constant.DataStartDate + '"'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def drewPEDateLines():
    if not os.path.exists('./Data/Pics'):
        os.mkdir('./Data/Pics')
    HYCodes = getHYTypeFromDB('pe_data')
    for code in HYCodes:
        data = getHYDataFromDB('pe_data', code['hy_code'])
        lineNames = ['dynamicPE', 'MonthAvg', '3MonthAvg', '6MonthAvg','YearAvg']
        df = pandas.DataFrame(data)
        df.columns = data[0].keys()
        Ys = [df['dynamic_pe'], df['pe_avg_month'], df['pe_avg_3month'], df['pe_avg_6month'], df['pe_avg_year']]
        colors = ['red','blue','green','yellow','black']
        drawLine.drawLines(df['date'], Ys, lineNames, colors ,'PE-'+ code['hy_code'], './Data/Pics/' + df['hy_name'][0]).close()

def getPEDataLinesData(hycode):
    data = getHYDataFromDB('pe_data', hycode)
    lineNames = ['dynamicPE', 'MonthAvg', '3MonthAvg', '6MonthAvg','YearAvg']
    df = pandas.DataFrame(data)
    df.columns = data[0].keys()
    df['date'] = df.apply(lambda x: x['date'].strftime('%Y%m%d'), axis=1)
    Ys = [df['dynamic_pe'].tolist(), df['pe_avg_month'].tolist(), df['pe_avg_3month'].tolist(), df['pe_avg_6month'].tolist(), df['pe_avg_year'].tolist()]
    colors = ['red','blue','green','yellow','black']
    value = {'industry_id':hycode, 'values':{'lineNames':lineNames, 'x':df['date'].tolist(),'Ys':Ys, 'colors': colors}}
    return value
    
def calcIndustryValue():
    global calcedIndustryPE
    signTime = datetime.datetime.strptime(calcedIndustryPE['time'].strftime('%Y-%m-%d') + " 17:30:00", '%Y-%m-%d %H:%M:%S')
    if len(calcedIndustryPE['data']) > 0 and (datetime.datetime.now() < signTime or calcedIndustryPE['time'] > signTime):
        return calcedIndustryPE['data']
    calcedIndustryPE['data'].clear()
    result: List[Any] = []
    sql = 'select dynamic_pe, hy_code, hy_name, stocknum, lostnum  from pe_data where date=(select max(date) from pe_data) and stocknum>0'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchALL(conn, sql)
    for row in ret:
        sql = 'select count(pe.dynamic_pe <= ' + str(row['dynamic_pe']) + '  or null) AS pos, count(*) total from pe_data pe \
            where pe.hy_code = ' + str(row['hy_code'])
        data = mysqlOp.fetchOne(conn, sql)
        temperature = float('%.1f' %(data['pos']*100/data['total']))
        sql = 'select GROUP_CONCAT(CONCAT(" ",name," ")) from stock_info where level4_hy_code =' + str(row['hy_code']) + ' and name \
            in (select name from zz800list where date=(select max(date) from zz800list))'
        stocks = mysqlOp.fetchOne(conn, sql)
        value = {'industry_id':row['hy_code'], 'industry_name':row['hy_name'], 'pe':row['dynamic_pe'], 'pe_temperature': temperature, 
                    'stock_num':row['stocknum'], 'lost_num':row['lostnum'], 'stocks': stocks[0]}
        result.append(value)
    conn.close()
    calcedIndustryPE['time'] = datetime.datetime.now()
    calcedIndustryPE['data'] = result
    return result

def getLastDate():
    sql = 'select tb.date from pe_data tb order by tb.date DESC'
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchOne(conn, sql)
    conn.close()
    return ret

def getStockInfo(dateName):
    fileName = 'csi' + dateName + '.zip'
    unzip(makePEFilePath(dateName) + fileName)
    print('will save stock_info: ', dateName)
    fileName = 'csi' + dateName + '.xls'
    saveData(readStockInfoData(fileName), dateName, 'stock_info', 'replace')
    if os.path.exists('./Data/tmp/'+fileName):
        os.remove('./Data/tmp/'+fileName)

def getStockInfoWithCode(stockCode):
    sql = 'select * from stock_info where code=' + stockCode
    conn = mysqlOp.connectMySQL()
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def getPEData(endDate):
    createPETable()
    createPBTable()
    createDYRTable()
    createStockInfo()
    if not os.path.exists('./Data'):
        os.mkdir('./Data')
    if not os.path.exists('./Data/tmp/'):
        os.mkdir('./Data/tmp/')
    '''startDate is the lastest date read form db . if is none it's the date five years ago'''
    startDate = getLastDate()
    if startDate is None:
        startDate = datetime.datetime.strptime(constant.DataStartDate, '%Y-%m-%d').date()
    else:
        startDate = startDate[0]
    print('start date: ', startDate, ' endDate: ', endDate)
    dateNameList=[]
    for i in range((endDate - startDate).days + 1):
        dateName = (startDate + datetime.timedelta(days=i)).strftime('%Y%m%d')
        if isDataExist(dateName, 'pe_data') and isDataExist(dateName, 'dyr_data') and isDataExist(dateName, 'pb_data'):
            continue
        fileName = 'csi' + dateName + '.zip'
        if downloadPEDataFile(fileName, dateName):
            dateNameList.append(dateName)
            fileName = 'csi' + dateName + '.xls'
            print('will save pe&pb&dyr date: ', dateName)
            saveData(readPEData(fileName), dateName, 'pe_data', 'append')
            saveData(readPBData(fileName), dateName, 'pb_data', 'append')
            saveData(readDYRData(fileName), dateName, 'dyr_data', 'append')
            if os.path.exists('./Data/tmp/'+fileName):
                os.remove('./Data/tmp/'+fileName)
    # get lasted stocked info
    if len(dateNameList) > 0:
        dateName = dateNameList.pop()
        getStockInfo(dateName)