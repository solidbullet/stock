from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from pymongo import MongoClient
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
auth('13818571403','Jyq810302')


sdate = '2019-03-27'
edate = '2019-03-28'

# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')
mycol = db['origin']


df = pd.read_csv("c:\\stock\\list\\20190327.csv",dtype=str,encoding="ANSI")

dict_df = pd.DataFrame()
for index, row in df.iterrows():
    stockid = normalize_code(row['id'].zfill(6))

    df = get_price(stockid, start_date=sdate, end_date=edate, frequency='daily')
    df['rise'] = 100 * df['close'].pct_change().fillna(0)
    rise = df['rise'].iloc[-1]
    name = get_security_info(stockid).display_name
    # volumn = df['money'].iloc[-1] / 100000000
    # dict1 = {'id':[stockid],'name':[name],'diff30':[diff30],'ratio':[ratio],'volumn':[volumn],'lianban':[lianban],'rise':[rise]}
    dict1 = {'id': [stockid], 'name': [name], 'rise': [rise]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)
dragon = dict_df.sort_values(by = 'rise',ascending = False)
print(dragon)


#大盘指数
# stocks = ['000001.XSHG','399001.XSHE','399300.XSHE','000905.XSHG','000016.XSHG','000010.XSHG','000009.XSHG','399007.XSHE','399011.XSHE']
# for x in stocks:
#     df = get_price(x, start_date=sdate, end_date=edate, frequency='daily')
#     df['rise'] = 100 * df['close'].pct_change().fillna(0)
#     rise = df['rise'].iloc[-1]
#     name = get_security_info(x).display_name
#     print("%s: 涨幅是:%.2f%%" %(name,rise))

