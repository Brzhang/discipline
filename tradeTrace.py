from pandas import DataFrame
import datetime
import stock_strategy

totalMoney = 100000
recodeDF = DataFrame(columns=['code', 'name', 'price', 'vol', 'date', 'opt'])

def beginTrace(startDate, endDate):
    start = datetime.datetime.strptime(startDate, '%Y-%m-%d').date() + datetime.timedelta(days=120)
    end = datetime.datetime.strptime(endDate, '%Y-%m-%d').date()
    for i in range((end - start).days + 1):
        endday = (start + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        stock_strategy.calcMASystem(start.strftime('%Y-%m-%d'), endday, True)

def recordTrade(code, name, price, vol, date, opt):
    print(code, name, price, vol, date, opt)
    global recodeDF
    if vol > 0:
        dict = {'code': code, 'name' : name, 'pirce' : price, 'vol' : int((totalMoney*vol/price)/100)*100, 'date' : date, 'opt' : opt}
    else:
        dict = {'code': code, 'name' : name, 'pirce' : price, 'vol' : vol, 'date' : date, 'opt' : opt}
    data = DataFrame(list(dict.items()))
    print('record trade: ', data)
    recodeDF = recodeDF.append(data, ignore_index=True)

def getPositionList():
    return getPositionDF().values

def getPositionDF():
    global recodeDF
    merged = recodeDF.groupby(by=['code'])['vol'].sum().to_frame()
    merged.drop(merged[merged['vol'].apply(lambda x: x==0)].index, inplace=True)
    print('trade position: ', merged)
    return merged

def showTradeList():
    global recodeDF
    return '{' + getPositionDF().to_json(orient="records", force_ascii = False) + ',' + recodeDF.to_json(orient="records", force_ascii = False) + '}'