
import datetime
import pandas

DataStartDate='2017-01-01'
fileType='png'
drawDpi=200
HQServerIP='119.147.212.81'
HQServerPort=7709
EXHQServerIP='112.74.214.43'
EXHQServerPort=7727
PEDataUrl='http://47.97.204.47/syl/'
ZZ800fileUrl='http://www.csindex.com.cn/uploads/file/autofile/cons/000906cons.xls'
ZZ800fileDownloadHeaders={
    'Host': 'www.csindex.com.cn',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'}
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