from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
import warnings
from pymongo import MongoClient
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
auth('13818571403','Jyq810302')


today = '2019-03-14'
tdate= datetime.datetime.strptime(today,"%Y-%m-%d")
delta = datetime.timedelta(days=30)  #取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
n_days = tdate - delta
yesterday = n_days.strftime('%Y-%m-%d')  #从今天往前面数1天的日期

stock = '600818.XSHG'
#stocks = list(get_all_securities(['stock']).index)
stocks = ['601865.XSHG','600604.XSHG','002600.XSHE','000409.XSHE','000631.XSHE','000048.XSHE']

# dict_df = pd.DataFrame()
# for x in stocks:
#     df = get_price(x, start_date=yesterday, end_date=today, frequency='daily')
#     vibration = (df['high'].max() - df['low'].min()) / df['low'].min()
#     dict = {'id': [x],'vibration': [ vibration]}
#     d = pd.DataFrame(dict)
#     dict_df = dict_df.append(d)
# dragon = dict_df.sort_values(by = 'vibration',ascending = False)
# print(dragon)


client=MongoClient("localhost",27017)
db=client.stock
mycol = db['store']
myquery = {"start_date": {"$lt": yesterday}}
mydoc = mycol.find(myquery,{'stock_id':1,'_id':0,'stock_name':1})

dict_df = pd.DataFrame()

for x in mydoc:
    id = x['stock_id']
    name = x['stock_name']
    df = get_price(id, start_date=yesterday, end_date=today, frequency='daily')
    vibration = (df['high'].max() - df['low'].min()) / df['low'].min()
    dict = {'id': [id], 'name': [name],'vibration': [ vibration]}
    d = pd.DataFrame(dict)
    dict_df = dict_df.append(d)
dragon = dict_df.sort_values(by = 'vibration',ascending = False)
print(dragon)
dict_df.to_csv('c:\\stock\\'+today+'vibration.csv')