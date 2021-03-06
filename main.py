import getPEData
import getZZ800Data
import stock_strategy
import jisilu_data
import trade
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import time
from flask import Flask, Blueprint, render_template, jsonify, request
import constant
import flask_cors
import socket
import _thread

app = Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)
service = Blueprint('discipline', __name__, static_folder='./web', template_folder='./web')

@service.route('/update', methods=['GET'])
def updateDB():
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

def scheduleDailyData():
    _thread.start_new_thread(getPEData.getPEData,(constant.get_last_weekday(),))
    _thread.start_new_thread(getZZ800Data.getZZ800List,())
    jisilu_data.get_jsl_dividend_rate()
    jisilu_data.get_jsl_convert_bond_data()
    jisilu_data.get_jsl_temperature()
    print(datetime.datetime.now())

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
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduleDailyData, 'cron', hour=17, minute=30)
    scheduler.start()

    app.register_blueprint(service)
    app.run(host=get_host_ip(), port=8089, debug=True)