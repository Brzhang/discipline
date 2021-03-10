import talib
import numpy
from pandas import DataFrame
import getZZ800Data as zz800

def MVAvgSystem():
    # get zz800 list
    stockList = zz800.getZZ800CodeList()
    for stock in stockList:
        data = DataFrame(zz800.getStockKData('c' + stock[0]))
        data.columns = ['data_id', 'code', 'open', 'close', 'high', 'low', 'vol', 'amount', 'date']
        data['MA5'] = talib.MA(numpy.array(data['close']), timeperiod = 5)
        data['MA10'] = talib.MA(numpy.array(data['close']), timeperiod = 10)
        data['MA20'] = talib.MA(numpy.array(data['close']), timeperiod = 20) 
        data['MA60'] = talib.MA(numpy.array(data['close']), timeperiod = 60)
        data['MA120'] = talib.MA(numpy.array(data['close']), timeperiod = 120)
        print(data)