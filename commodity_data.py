from pytdx.exhq import TdxExHq_API
import pandas
import mysqlOp
import datetime
import constant

def getCommodity():
    api = TdxExHq_API()
    if api.connect(constant.EXHQServerIP, constant.EXHQServerPort):
        print('EXHQ connect')
        data = api.get_instrument_info(0, 1000)
        print(data)
        #data = api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 37, 'oil, 0, 1000)
        api.disconnect()
    else:
        print('EXHQ disconnect')