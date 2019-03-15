from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
auth('13818571403','Jyq810302')


edate = '2019-03-11'
tdate= datetime.datetime.strptime(edate,"%Y-%m-%d")
delta = datetime.timedelta(days=5)  #取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
n_days = tdate - delta
sdate = n_days.strftime('%Y-%m-%d')  #从今天往前面数35天的日期

#stocks = list(get_all_securities(['stock']).index)
#stocks = ['601865.XSHG','600604.XSHG','002600.XSHE','000409.XSHE','000631.XSHE','000048.XSHE']

df = pd.read_csv("c:\\stock\\index.csv",dtype=str,encoding="ANSI")

dict_df = pd.DataFrame()
for index, row in df.iterrows():
    stockid = normalize_code(row['id'])
    df = get_price(stockid, start_date=sdate, end_date=edate, frequency='daily')
    df['rise'] = 100 * df['close'].pct_change().fillna(0)
    rise = df['rise'].iloc[-1]
    name = row['name']
    dict1 = {'id':[stockid],'name':[name],'rise':[rise]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)
dragon = dict_df.sort_values(by = 'rise',ascending = False)
print(dragon)

# stocks = ['399001.XSHE','000001.XSHG','000016.XSHG','000010.XSHG','000009.XSHG','000905.XSHG','399007.XSHE','399011.XSHE','399300.XSHE']
# for x in stocks:
#     df = get_price(x, start_date=sdate, end_date=edate, frequency='daily')
#     df['rise'] = 100 * df['close'].pct_change().fillna(0)
#     rise = df['rise'].iloc[-1]
#     name = get_security_info(x).display_name
#     print("%s: 涨幅是:%.2f%%" %(name,rise))


