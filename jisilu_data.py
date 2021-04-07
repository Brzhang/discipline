# !/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Any
import pandas
import urllib.request
import json
import re
import mysqlOp
import datetime
import constant

def isDataExist(dateName, table):
    conn = mysqlOp.connectMySQL()
    sql = 'select count(*) count from ' + table + ' where date=' + dateName
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    if ret[0]['count'] > 0:
        return True
    else:
        return False

def saveData(data, table, type):
    if data is None:
        return
    if isDataExist(data['date'][0].strftime('%Y%m%d'), table):
        return
    conn = mysqlOp.connectMySQL()
    data.to_sql(name=table, con = conn, if_exists=type, index=False)
    conn.close()

def create_dividend_rate_table():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'dividend_rate (data_id INT(11) AUTO_INCREMENT, stock_id VARCHAR(45) DEFAULT NULL, stock_nm VARCHAR(45) DEFAULT NULL,\
            price FLOAT DEFAULT 0.0, increase_rt FLOAT DEFAULT 0.0, volume FLOAT DEFAULT 0.0, total_value FLOAT DEFAULT 0.0,\
            pe FLOAT DEFAULT 0.0, pe_temperature FLOAT DEFAULT 0.0, pb FLOAT DEFAULT 0.0, pb_temperature FLOAT DEFAULT 0.0,\
            aft_divided FLOAT DEFAULT 0.0, dividend_rate FLOAT DEFAULT 0.0, dividend_rate2 FLOAT DEFAULT 0.0, roe FLOAT DEFAULT 0.0,\
            roe_average FLOAT DEFAULT 0.0, revenue_average FLOAT DEFAULT 0.0, profit_average FLOAT DEFAULT 0.0, cashflow_average FLOAT DEFAULT 0.0,\
            dividend_rate_average FLOAT DEFAULT 0.0, eps_growth_ttm FLOAT DEFAULT 0.0, init_debt_rate FLOAT DEFAULT 0.0,\
            industry_nm FLOAT DEFAULT 0.0, date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def create_convert_bond_table():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'convert_bond (data_id INT(11) AUTO_INCREMENT, bond_id VARCHAR(45) DEFAULT NULL, bond_nm VARCHAR(45) DEFAULT NULL,\
            price FLOAT DEFAULT 0.0, increase_rt FLOAT DEFAULT 0.0, stock_nm VARCHAR(45) DEFAULT NULL, sprice FLOAT DEFAULT 0.0,\
            sincrease_rt FLOAT DEFAULT 0.0, pb FLOAT DEFAULT 0.0, convert_price FLOAT DEFAULT 0.0, convert_value FLOAT DEFAULT 0.0,\
            premium_rt FLOAT DEFAULT 0.0, rating_cd FLOAT DEFAULT 0.0, force_redeem_price FLOAT DEFAULT 0.0,\
            date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def create_jsl_temperature_table():
    conn = mysqlOp.connectMySQL()
    tbInfo = 'jsl_temperature (data_id INT(11) AUTO_INCREMENT, median_pb FLOAT DEFAULT 0.0,\
            median_pb_temperature FLOAT DEFAULT 0.0, median_pe FLOAT DEFAULT 0.0, median_pe_temperature FLOAT DEFAULT 0.0,\
            stock_count FLOAT DEFAULT 0.0, IPO_count FLOAT DEFAULT 0.0, st_count FLOAT DEFAULT 0.0, index_point FLOAT DEFAULT 0.0,\
            date DATE, PRIMARY KEY (data_id))ENGINE=InnoDB DEFAULT CHARSET=utf8'
    mysqlOp.createTable(conn, tbInfo)
    conn.close()

def get_jsl_dividend_rate_from_db():
    return get_data_from_db('dividend_rate')

def get_jsl_convert_bond_from_db():
    return get_data_from_db('convert_bond')

def get_jsl_temperature_from_db():
    return get_data_from_db('jsl_temperature')

def get_data_from_db(table):
    conn = mysqlOp.connectMySQL()
    sql = 'SELECT * from ' + table + ' where date=(select max(date) from ' + table + ')'
    ret = mysqlOp.fetchALL(conn, sql)
    conn.close()
    return ret

def convert_divident_rete_data_json(data):
    columns = ['stock_id', 'stock_nm', 'price', 'increase_rt', 'volume', 'total_value','pe', 'pe_temperature', 'pb', 'pb_temperature',
                'aft_dividend', 'dividend_rate', 'dividend_rate2', 'roe', 'roe_average', 'revenue_average', 'profit_average',
                'cashflow_average', 'dividend_rate_average', 'eps_growth_ttm', 'int_debt_rate', 'industry_nm', 'date']
    return constant.convertDBToJson(data, columns)

def convert_jsl_convert_bond_data_json(data):
    columns = ['bond_id', 'bond_nm', 'price', 'increase_rt', 'stock_nm', 'sprice','sincrease_rt', 'pb', 'convert_price', 'convert_value', 'premium_rt',
                'rating_cd', 'force_redeem_price', 'date']
    return constant.convertDBToJson(data, columns)

def convert_jsl_temperature_json(data):
    columns = ['price_dt', 'median_pb', 'median_pb_temperature', 'median_pe', 'median_pe_temperature', 'stock_count', 'IPO_count', 'st_count', 'index_point', 'date']
    return constant.convertDBToJson(data, columns)

def get_jsl_dividend_rate():
    """
    get the dividend rate from www.jisilu.cn and store to database
    :return:
    """
    create_dividend_rate_table()
    jsl_dividend_rate_url = 'https://www.jisilu.cn/data/stock/dividend_rate_list/'
    dividend_rate_text = urllib.request.urlopen(jsl_dividend_rate_url).read()

    dividend_rate_json = json.loads(dividend_rate_text)
    dividend_rate_list: List[Any] = []
    for item in dividend_rate_json['rows']:
        dividend_rate_list.append(item['cell'])
    dividend_rate_df = pandas.DataFrame(dividend_rate_list)

    # dividend_rat_df.pop('index')
    '''代码，名称，价格，涨幅，成交额(万)，市值，
    PE TTM，PE温度，pb，pb温度，
    5年均股息率，股息率，静态股息率，
    最新年报ROE，5年均ROE，5年营收增长，5年利润增长，
    5年现金流增长，5年分红率增长，净利同比增长，有息负债率，
    行业名称'''
    dividend_rate_df = dividend_rate_df[['stock_id', 'stock_nm', 'price', 'increase_rt', 'volume', 'total_value',
                                       'pe', 'pe_temperature', 'pb', 'pb_temperature',
                                       'aft_dividend', 'dividend_rate', 'dividend_rate2',
                                       'roe', 'roe_average', 'revenue_average', 'profit_average',
                                       'cashflow_average', 'dividend_rate_average', 'eps_growth_ttm', 'int_debt_rate',
                                       'industry_nm']]
    dividend_rate_df['date'] = datetime.date.today()
    saveData(dividend_rate_df, 'dividend_rate', 'replace')

def get_jsl_convert_bond_data():
    """
    get convert bond data from www.jisilu.cn and store to database
    :return:
    """
    create_convert_bond_table()

    jsl_convert_bond_url = 'https://www.jisilu.cn/data/cbnew/cb_list/'
    convert_bond_data_text = urllib.request.urlopen(jsl_convert_bond_url).read()

    convert_bond_json = json.loads(convert_bond_data_text)
    convert_bond_list: List[Any] = []
    for item in convert_bond_json['rows']:
        convert_bond_list.append(item['cell'])
    convert_bond_df = pandas.DataFrame(convert_bond_list)

    '''转债代码，转债名称，现价，涨跌幅，正股名，正股价，
    正股涨跌，pb，转股价，转股价值，溢价率，
    评级，强赎触发价'''
    convert_bond_df = convert_bond_df[['bond_id', 'bond_nm', 'price', 'increase_rt', 'stock_nm', 'sprice',
                                       'sincrease_rt', 'pb', 'convert_price', 'convert_value', 'premium_rt',
                                       'rating_cd', 'force_redeem_price']]
    convert_bond_df['date'] = datetime.date.today()

    saveData(convert_bond_df, 'convert_bond', 'replace')

def get_jsl_temperature():
    """
    get the temperature of pb and pe form jisilu
    :return:
    """

    create_jsl_temperature_table()
    '''{"price_dt":"2021-04-01","median_pb":"2.36","median_pb_temperature":"22.82","median_pe":"28.14","median_pe_temperature":"24.95","stock_count":"3583.00","IPO_count":"496.00","st_count":"190.00","index_point":"5487.70"}'''
    jsl_url = 'https://www.jisilu.cn/data/indicator/get_last_indicator/'
    jsl_content_text = urllib.request.urlopen(jsl_url).read()
    temperature_json = json.loads(jsl_content_text)
    temperature_df = pandas.DataFrame(temperature_json, index=[0])

    temperature_df = temperature_df[['price_dt', 'median_pb', 'median_pb_temperature', 'median_pe', 'median_pe_temperature', 'stock_count',
                                       'IPO_count', 'st_count', 'index_point']]
    temperature_df.rename(columns={'price_dt':'date'}, inplace = True)
    temperature_df['date'] = temperature_df.apply(lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d').date(), axis=1)

    saveData(temperature_df, 'jsl_temperature', 'append')
