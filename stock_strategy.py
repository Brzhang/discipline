import talib
import numpy
from pandas import DataFrame
import time
import datetime
import getZZ800Data as zz800
import getPEData as PEdata
import drawLine
import constant
import trade

dictResult = {'time': datetime.datetime.now(), 'data': []}

def calcMA(data, days):
    data['MA' + str(days)] = talib.MA(numpy.array(data['close']), timeperiod = days)

def keep_float_value_dot_3(data, col_name):
    data[col_name] =  data.apply(lambda x: constant.f_dot_3(x[col_name]), axis=1)

def date_to_string(data, col_name):
    data[col_name] =  data.apply(lambda x: x[col_name].strftime('%Y%m%d'), axis=1)

def MASystem():
    global dictResult
    signTime = datetime.datetime.strptime(dictResult['time'].strftime('%Y-%m-%d') + " 17:30:00", '%Y-%m-%d %H:%M:%S')
    if len(dictResult['data']) > 0 and (datetime.datetime.now() < signTime or dictResult['time'] > signTime):
        return dictResult['data']
    dictResult['data'].clear()
    # get zz800 list
    stockList = zz800.getZZ800CodeList()
    result: List[Any] = []
    positionList = trade.getPositionList()
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

        lastIndex = len(data)-1
        price = data.at[lastIndex,'close']
        ma5 = data.at[lastIndex,'MA5']
        ma10 = data.at[lastIndex,'MA10']
        ma20 = data.at[lastIndex,'MA20']
        ma60 = data.at[lastIndex,'MA60']
        ma120 = data.at[lastIndex,'MA120']
        inPosition = False
        for position in positionList:
            if(stock[0] == position[0]):
                inPosition = True
                if ma5 - data.at[lastIndex-1, 'MA5'] < 0:
                    stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]
                    result.append(makeTradeData(stockInfo, data, 'sell0', 0.3, price, lastIndex))
                    trade.recordTrade(stockInfo[1], stockInfo[2], price, -1*position[1], data.at[lastIndex, 'date'], 'sell0')
                elif ma10 > ma20:
                    stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]
                    result.append(makeTradeData(stockInfo, data, 'buy2', 0.7, price, lastIndex))
                    trade.recordTrade(stockInfo[1], stockInfo[2], price, 0.7, data.at[lastIndex, 'date'], 'buy2')
                elif price < ma20:
                    stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]
                    result.append(makeTradeData(stockInfo, data, 'sell1', 0.5, price, lastIndex))
                    trade.recordTrade(stockInfo[1], stockInfo[2], price, -0.5*position[1], data.at[lastIndex, 'date'], 'sell1')
                elif ma5 < ma10:
                    stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]
                    result.append(makeTradeData(stockInfo, data, 'sell2', 1, price, lastIndex))
                    trade.recordTrade(stockInfo[1], stockInfo[2], price, -1*position[1], data.at[lastIndex, 'date'], 'sell2')
                break
        if inPosition == False:
            ''' 1、多均线集结在一起，30日、60日、90日均线之间幅度不超过5%。
                2、大阳线突破（5%当日涨幅），在这三条均线均价的4%-15%之间（起涨阶段）。
                3、长期均线（年线）走强，并且3条均线的均价即短期在长期均线之上。
                4、盘中自动弹出。
                MA30:=MA(C,30);MA60:=MA(C,60);MA90:=MA(C,90);
                MA250:=MA(C,250);
                A:=MAX(MA30,MAX(MA60,MA90));
                B:=MIN(MA30,MIN(MA60,MA90));
                E:=(MA30+MA60+MA90)/3;
                BUYHAOGU:A/B<1.05 AND C>E*1.04 AND C<E*1.15 AND MA250>REF(MA250,1) AND E>MA250 AND C/REF(C,1)>1.05;'''
            maxValue = max(ma20, ma60, ma120)
            minValue = min(ma20, ma60, ma120)
            avgValue = constant.f_dot_3((ma20+ma60+ma120)/3.0)
            deltaMA120 = ma120 - data.at[lastIndex-1, 'MA120']
            data['MAV120'] = talib.MA(numpy.array(data['amount']), timeperiod = 120)
            recent60Price = data['close'][3:-63].tolist()
            #if price > ma20 and ma20 > ma5 and ma5 > ma10 and ma20 > ma60 and \
            if maxValue/minValue < 1.05 and price > avgValue*1.04 and price < avgValue*1.1 and avgValue > ma120 and price > data.at[lastIndex-1,'close'] and \
                max(recent60Price) < min(recent60Price)*1.15 and deltaMA120 > 0 and data.at[lastIndex, 'amount'] > data.at[lastIndex,'MAV120']:
                stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]

                while(len(PEdata.calcedIndustryPE['data']) < 1):
                    time.sleep(1)
                industryPE = DataFrame(PEdata.calcedIndustryPE['data'])

                HYInfo = industryPE.loc[industryPE['industry_name']==stockInfo[4]].to_dict('records')[0]
                if((HYInfo['pe'] == 0 and HYInfo['pe_temperature']==100) or HYInfo['pe_temperature']<25.0):
                    date_to_string(data, 'date')
                    infoDic = {'opt':'buy1', 'vol':'0.3', 'code':stockInfo[1], 'name':stockInfo[2], 'price':price,
                            'HY': stockInfo[4], 'HYPE':HYInfo['pe'], 'HYPETemperature':HYInfo['pe_temperature'],
                            'dynamicPE':stockInfo[6], 'PE':stockInfo[5],'PB':stockInfo[7], '5Cost':data.at[lastIndex-5,'close'], '10Cost':data.at[lastIndex-10,'close'], 
                            '20Cost':data.at[lastIndex-20,'close'],'60Cost':data.at[lastIndex-60,'close'], '120Cost':data.at[lastIndex-120,'close'],
                            'values':makeChartData(data)}
                    result.append(infoDic)
                    trade.recordTrade(stockInfo[1], stockInfo[2], price, 0.3, data.at[lastIndex, 'date'], 'buy1')
                    #drawLine.drawLines(data['date'][120:], Ys, lineNames, colors ,'MA-' + stockInfo[0], './Data/Pics/'+stockInfo[0]+'_'+stockInfo[1]).close()
    dictResult['time'] = datetime.datetime.now()
    dictResult['data'] = result
    return result

def makeChartData(data):
    lineNames = ['price', 'MA5', 'MA10', 'MA20', 'MA60', 'MA120']
    Ys = [data[['open','close','high','low']][120:].values.tolist(), data['MA5'][120:].tolist(), data['MA10'][120:].tolist(), data['MA20'][120:].tolist(), data['MA60'][120:].tolist(), data['MA120'][120:].tolist()]
    colors = ['#5470c6','#91cc75','#fac858','#ee6666','#73c0de','#3ba272']
    return {'lineNames':lineNames, 'x':data['date'][120:].tolist(),'Ys':Ys, 'colors': colors}

def makeTradeData(stockInfo, data, opt, vol, price, lastIndex):
    while(len(PEdata.calcedIndustryPE['data']) < 1):
        time.sleep(1)
    industryPE = DataFrame(PEdata.calcedIndustryPE['data'])

    HYInfo = industryPE.loc[industryPE['industry_name']==stockInfo[4]].to_dict('records')[0]
    date_to_string(data, 'date')
    infoDic = {'opt':opt, 'vol':str(vol), 'code':stockInfo[1], 'name':stockInfo[2], 'price':price,
            'HY': stockInfo[4], 'HYPE':HYInfo['pe'], 'HYPETemperature':HYInfo['pe_temperature'],
            'dynamicPE':stockInfo[6], 'PE':stockInfo[5],'PB':stockInfo[7], '5Cost':data.at[lastIndex-5,'close'], '10Cost':data.at[lastIndex-10,'close'], 
            '20Cost':data.at[lastIndex-20,'close'],'60Cost':data.at[lastIndex-60,'close'], '120Cost':data.at[lastIndex-120,'close'],
            'values':makeChartData(data)}
    return infoDic