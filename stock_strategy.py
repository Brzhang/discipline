import talib
import numpy
from pandas import DataFrame
import getZZ800Data as zz800
import getPEData as PEdata
import drawLine

def MAAvgSystem():
    # get zz800 list
    stockList = zz800.getZZ800CodeList()
    for stock in stockList:
        print('will calc MAAvgSystem: ', stock[0])
        data = DataFrame(zz800.getStockKData('c' + stock[0]))
        data.columns = ['data_id', 'code', 'open', 'close', 'high', 'low', 'vol', 'amount', 'date']
        data['MA5'] = talib.MA(numpy.array(data['close']), timeperiod = 5)
        data['MA10'] = talib.MA(numpy.array(data['close']), timeperiod = 10)
        data['MA20'] = talib.MA(numpy.array(data['close']), timeperiod = 20) 
        data['MA60'] = talib.MA(numpy.array(data['close']), timeperiod = 60)
        data['MA120'] = talib.MA(numpy.array(data['close']), timeperiod = 120)
        lastIndex = len(data)-1
        price = data.at[lastIndex,'close']
        ma5 = data.at[lastIndex,'MA5']
        ma10 = data.at[lastIndex,'MA10']
        ma20 = data.at[lastIndex,'MA20']
        ma60 = data.at[lastIndex,'MA60']
        ma120 = data.at[lastIndex,'MA120']
        if price > ma20 and ma20 > ma5 and ma5 > ma10:
            stockInfo = PEdata.getStockInfoWithCode(stock[0])[0]
            print('** buy1/3 ** stock code:', stockInfo[1], ' name:', stockInfo[2], ' price:', price, ' HY:', stockInfo[3], 
            ' dynamicPE:', stockInfo[5], ' PE:', stockInfo[6], ' PB:', stockInfo[7], ' 5Cost:', data.at[lastIndex-5,'close'],
            ' 10Cost:', data.at[lastIndex-10,'close'], ' 20Cost:', data.at[lastIndex-20, 'close'], 
            ' 60Cost:', data.at[lastIndex-60,'close'], ' 120Cost:', data.at[lastIndex-120,'close'])
            ''' draw line '''
            lineNames = ['MA5', 'MA10', 'MA20', 'MA60','MA120']
            Ys = [data['MA5'][120:], data['MA10'][120:], data['MA20'][120:], data['MA60'][120:], data['MA120'][120:]]
            colors = ['red','blue','green','yellow','black']
            drawLine.drawLines(data['date'][120:], Ys, lineNames, colors ,'MA-' + stockInfo[1], './Data/Pics/' + stockInfo[1]).close()
