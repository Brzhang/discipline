import constant
import mysqlOp
from pandas import DataFrame
import datetime

totalMoney = 100000

def recordTrade(code, name, price, vol, date, opt):
    createTradeDB()
    conn = mysqlOp.connectMySQL()
    print(code , "   ", name, "   ", price, "   ", vol)
    sql = 'select count(*) count from trade_list where code="' + code + '" and date=' + date
    ret = mysqlOp.fetchALL(conn, sql)
    if ret[0]['count'] > 0:
        conn.close()
        return
    if vol > 0:
        sql = 'insert into trade_list(code,name,price,vol,date,opt) values("' + code + '","' + name + '","' + str(price) + '",' + str(int((totalMoney*vol/price)/100)*100) + ',' + date + ',"' + opt + '")'
    else:
        sql = 'insert into trade_list(code,name,price,vol,date,opt) values("' + code + '","' + name + '","' + str(price) + '",' + str(vol) + ',' + date + ',"' + opt + '")'
    mysqlOp.executeSQL(conn, sql)
    conn.close()

def createTradeDB():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'trade_list (data_id INT(11) AUTO_INCREMENT, code VARCHAR(10) DEFAULT NULL, name VARCHAR(16) DEFAULT NULL, \
        vol INT DEFAULT 0, price FLOAT DEFAULT 0.0, date DATE, opt VARCHAR(8) DEFAULT NULL, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def getPositionList():
    conn = mysqlOp.connectMySQL()
    sql = "set sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    mysqlOp.executeSQL(conn, sql)
    sql = 'select code, sum(vol) from trade_list where date < ' +  datetime.date.today().strftime('%Y-%m-%d') + ' group by code HAVING sum(vol) > 0'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def showTradeList():
    conn = mysqlOp.connectMySQL()
    sql = 'select * from trade_list order by date'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return convertTradeDataJson(ret)

def calcCurrentPosition():
    conn = mysqlOp.connectMySQL()
    sql = "set sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    mysqlOp.executeSQL(conn, sql)
    sql = 'select * from trade_list group by code HAVING sum(vol) > 0'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return convertTradeDataJson(ret)

def convertTradeDataJson(data):
    columns = ['data_id', 'code', 'name', 'vol', 'buyprice', 'date', 'opt']
    return constant.convertDBToJson(data, columns)