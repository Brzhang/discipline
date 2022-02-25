import getPEData
import getZZ800Data
import stock_strategy
import jisilu_data
import trade
import tradeTrace
import fcntl
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
from flask import Flask, Blueprint, render_template, jsonify, request
import constant
import flask_cors
import socket
#import _thread

app = Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)
service = Blueprint('discipline', __name__, static_folder='./web', template_folder='./web')
updating = False

@service.route('/update', methods=['GET'])
def updateDB():
    if not updating :
        scheduleDailyData()
    return ''

@service.route('/IndustryPE', methods=['GET'])
def showIndustryPE():
    print('showIndustryPE')
    ret = getPEData.calcIndustryValue()
    print(datetime.datetime.now())
    return jsonify({'result':ret})

@service.route('/IndustryPELinesData', methods=['GET'])
def showIndustryPELinesData():
    hycode = request.args.get('code')
    return getPEData.getPEDataLinesData(hycode)

@service.route('/MASystem', methods=['GET'])
def showMASystem():
    ret = stock_strategy.MASystem()
    print(datetime.datetime.now())
    return jsonify({'result':ret})

@service.route('/JSLData', methods=['GET'])
def showJSLData():
    ret = jisilu_data.convert_divident_rete_data_json(jisilu_data.get_jsl_dividend_rate_from_db())
    return ret

@service.route('/ConvertBond', methods=['GET'])
def showConvertBondData():
    ret = jisilu_data.convert_jsl_convert_bond_data_json(jisilu_data.get_jsl_convert_bond_from_db())
    return ret

@service.route('/JSLTemperature', methods=['GET'])
def showJSLTemperature():
    return jisilu_data.convert_jsl_temperature_json(jisilu_data.get_jsl_temperature_from_db())

@service.route('/PositionList', methods=['GET'])
def showPositionList():
    return trade.calcCurrentPosition()

@service.route('/TradeList', methods=['GET'])
def showTradeList():
    return trade.showTradeList()

@service.route('/TradeTrace' , methods=['GET'])
def showTrace():
    #tradeTrace.beginTrace('2017-01-01', datetime.date.today().strftime('%Y-%m-%d'))
    tradeTrace.recordTrade('000001', 'name', 12.0, 0.3, '2021-02-01', 'buy1')
    tradeTrace.recordTrade('000001', 'name', 11.8, -2500, '2021-03-01', 'sell0')
    tradeTrace.recordTrade('000002', 'name1', 8.0, 0.3, '2021-03-01', 'buy1')
    return tradeTrace.getPositionDF().to_json(orient="records", force_ascii = False) 
    #return tradeTrace.showTradeList()

def scheduleDailyData():
    updating = True
    #_thread.start_new_thread(getPEData.getPEData,(constant.get_last_weekday(),))
    getPEData.getPEData(constant.get_last_weekday(datetime.date.today()))
    #_thread.start_new_thread(getZZ800Data.getZZ800List,())
    getZZ800Data.getZZ800List()
    jisilu_data.get_jsl_dividend_rate()
    jisilu_data.get_jsl_convert_bond_data()
    jisilu_data.get_jsl_temperature()
    print('get jisilu data completed. ' , datetime.datetime.now())
    updating = False

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        print(ip)
    finally:
        s.close()
    return ip

if __name__=='__main__':
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler = BackgroundScheduler()
        scheduler.add_job(scheduleDailyData, 'cron', day_of_week='mon-fri', hour=17, minute=00)
        scheduler.start()
    except:
        pass
    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
    atexit.register(unlock)

    app.register_blueprint(service)
    app.run(host=get_host_ip(), port=8089, debug=True)