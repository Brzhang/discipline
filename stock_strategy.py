import talib
import numpy
from pandas import DataFrame
import getZZ800Data as zz800
import getPEData as PEdata
import drawLine
import constant
import time

def calcMA(data, days):
    data['MA' + str(days)] = talib.MA(numpy.array(data['close']), timeperiod = days)

def keep_float_value_dot_3(data, col_name):
    data[col_name] =  data.apply(lambda x: constant.f_dot_3(x[col_name]), axis=1)

def date_to_string(data, col_name):
    data[col_name] =  data.apply(lambda x: x[col_name].strftime('%Y%m%d'), axis=1)

def MASystem():
    # get zz800 list
    stockList = zz800.getZZ800CodeList()
    result: List[Any] = []
    for stock in stockList:
        print('will calc MASystem: ', stock[0])
        data = DataFrame(zz800.getStockKData('c' + stock[0]))
        data.columns = ['data_id', 'code', 'open', 'close', 'high', 'low', 'vol', 'amount', 'date']
        calcMA(data, 5)
        calcMA(data, 10)
        calcMA(data, 20)
        calcMA(data, 60)
        calcMA(data, 120)
        keep_float_value_dot_3(data, 'MA5')
        keep_float_value_dot_3(data, 'MA10')
        keep_float_value_dot_3(data, 'MA20')
        keep_float_value_dot_3(data, 'MA60')
        keep_float_value_dot_3(data, 'MA120')

        date_to_string(data, 'date')

        lastIndex = len(data)-1
        price = data.at[lastIndex,'close']
        ma5 = data.at[lastIndex,'MA5']
        ma10 = data.at[lastIndex,'MA10']
        ma20 = data.at[lastIndex,'MA20']
        ma60 = data.at[lastIndex,'MA60']
        ma120 = data.at[lastIndex,'MA120']
        if price > ma20 and ma20 > ma5 and ma5 > ma10:
            stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]
            
            lineNames = ['MA5', 'MA10', 'MA20', 'MA60','MA120']
            Ys = [data['close'][120:].tolist(), data['MA5'][120:].tolist(), data['MA10'][120:].tolist(), data['MA20'][120:].tolist(), data['MA60'][120:].tolist(), data['MA120'][120:].tolist()]
            colors = ['purple','red','blue','green','yellow','black']

            while(PEdata.calcedIndustryPE.empty):
                time.sleep(1)

            HYInfo = PEdata.calcedIndustryPE.loc[PEdata.calcedIndustryPE['industry_name']==stockInfo[4]].to_dict('records')[0]
            if((HYInfo['pe'] == 0 and HYInfo['pe_temperature']==100) or HYInfo['pe_temperature']<25.0):
                infoDic = {'opt':'buy', 'vol':'0.3', 'code':stockInfo[1], 'name':stockInfo[2], 'price':price,
                        'HY': stockInfo[4], 'HYPE':HYInfo['pe'], 'HYPETemperature':HYInfo['pe_temperature'],
                        'dynamicPE':stockInfo[6], 'PE':stockInfo[5],'PB':stockInfo[7], '5Cost':data.at[lastIndex-5,'close'], '10Cost':data.at[lastIndex-10,'close'], 
                        '20Cost':data.at[lastIndex-20,'close'],'60Cost':data.at[lastIndex-60,'close'], '120Cost':data.at[lastIndex-120,'close'],
                        'values':{'lineNames':lineNames, 'x':data['date'][120:].tolist(),'Ys':Ys, 'colors': colors}}
                result.append(infoDic)
            #drawLine.drawLines(data['date'][120:], Ys, lineNames, colors ,'MA-' + stockInfo[0], './Data/Pics/'+stockInfo[0]+'_'+stockInfo[1]).close()
    return result
