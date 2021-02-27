from sqlalchemy import create_engine

#connect db
def connectMySQL():
    engine = create_engine('mysql+pymysql://root:zjt841110@localhost:3306/discipline?charset=utf8')
    return engine.connect()

#execute SQL
def executeSQL(conn, sql):
    conn.execute(sql)

#fetchALL data
def fetchALL(conn, sql):
    result = conn.execute(sql)
    return result.fetchall()

#fetchone data
def fetchOne(conn, sql):
    result = conn.execute(sql)
    return result.fetchone()

#close db
def closeMySQL(conn):
    conn.close()

def createDB(conn, dbName):
    if dbName is not None and dbName != '':
        sql = 'CREATE DATABASE [IF NOT EXISTS] ' + dbName
        executeSQL(conn, sql)
    else:
        print('the [{}] is empty or equal None!'.format(dbName))

def dropTable(conn, tbName):
    if tbName is not None and tbName != '':
        sql = 'DROP TABLE IF EXISTS ' + tbName
        executeSQL(conn, sql)
    else:
        print('the [{}] is empty or equal None!'.format(tbName))

def createTable(conn, tbName):
    if tbName is not None and tbName != '':
        sql = 'CREATE TABLE IF NOT EXISTS ' + tbName
        executeSQL(conn, sql)
    else:
        print('the [{}] is empty or equal None!'.format(tbName))

