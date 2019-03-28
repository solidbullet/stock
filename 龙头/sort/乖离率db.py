#!/usr/bin/env python
# -*- coding:utf8 -*-
from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
from pymongo import MongoClient
import redis
auth('13818571403','Jyq810302')

def cal_ban_num( stock,begindate,enddate ): #计算连板数量
    df = get_price(stock, start_date=begindate, end_date=enddate, frequency='daily')
    df['rise'] = df['close'].pct_change().fillna(0)
    i = 0
    while i < len(df):
        #print(df['rise'][len(df) - i - 1])

        if df['rise'][len(df) - i - 1] < 0.09:
            break
        i += 1
    return i

def get_ratio(df): #计算均值回归系数
    if df.empty:
        return 0
    b = df.sort_index(axis = 0,ascending = True)
    r = b.rolling(window = 30,min_periods = 1)
    ma30 = r['close'].aggregate(np.mean)
    std = r['close'].aggregate(np.std)
    #var = r['close'].aggregate(np.var)
    b['ma30'] = ma30
    b['std'] = std
    b['ratio'] = (b['close'] - b['ma30']) /b['std']
    b['diff30'] = b['close'] - b['ma30']
    res = [b.iloc[-1]['ratio'],b.iloc[-1]['diff30']] # ratio 考虑了std的均值回归，diff30不考虑std
    # print(b.iloc[-1]['ratio'])
    return res

# stock = '603729.XSHG'
edate = '2019-03-20'
tdate= datetime.datetime.strptime(edate,"%Y-%m-%d")
delta = datetime.timedelta(days=35)  #取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
n_days = tdate - delta
sdate = n_days.strftime('%Y-%m-%d')  #从今天往前面数35天的日期


client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')

date = "2019-03-21"
dict_df = pd.DataFrame()

mycol = db['origin']
myquery = {"date":date}
mydoc = mycol.find(myquery).sort("rise",-1)
print(mydoc.count())
for x in mydoc:
    stockid = x['stock_id']
    stockname = x['stock_name']
    lianban_num = x['lianban']
    ratio = round(x['ratio'],2)
    diff30 = round(x['diff30'],2)
    volumn = round(x['volumn'],2)
    rise = round(x['rise'], 2)
    reback  = x['reback']
    vibration = x['vibration']
    market = x['market']
    vol_d_mar = round(volumn/market,2)

    dict1 = {'id': [stockid], 'name': [stockname], 'diff30':[diff30],'ratio':[ratio],'volumn':[volumn],'reback':[reback],'vibration':[vibration],'market':[market],'vol_d_mar':[vol_d_mar],'rise': [rise]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)
# for item in col.find():
dragon = dict_df.sort_values(by = 'ratio',ascending = False)
print (dragon)
# dragon = dragon[(dragon['lianban'] >= 2) &(dragon['lianban'] <= 4)]
dragon.to_csv('c:\\stock\\'+date+'ratio.csv')
#关闭连接
client.close()

