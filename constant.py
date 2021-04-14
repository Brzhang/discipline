
import datetime
import pandas

DataStartDate='2017-01-01'
fileType='png'
drawDpi=200
HQServerIP='119.147.212.81'
HQServerPort=7709
EXHQServerIP='61.152.107.141'
EXHQServerPort=7727
PEDataUrl='http://47.97.204.47/syl/'
ZZ800fileName = '000906cons.xls'

def get_last_weekday(day=datetime.date.today()):
    """
    get the last weekday which given day, today is the default if not given
    :param day:
    :return:
    """
    if day.isoweekday() > 5:
        return day - datetime.timedelta(days=(day.isoweekday()-5))
    return day


def f_dot_3(num):
    return float('%.3f' % num)

def convertDBToDF(ret, columns):
    data = pandas.DataFrame(list(ret))
    data.columns = columns
    if 'date' in columns:
        data['date'] =  data.apply(lambda x: x['date'].strftime('%Y-%m-%d'), axis=1)
    return data

def convertDBToJson(ret, columns):
    return convertDBToDF(ret, columns).to_json(orient="records", force_ascii = False)