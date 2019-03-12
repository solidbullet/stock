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
edate = '2019-03-12'
tdate= datetime.datetime.strptime(edate,"%Y-%m-%d")
delta = datetime.timedelta(days=35)  #取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
n_days = tdate - delta
sdate = n_days.strftime('%Y-%m-%d')  #从今天往前面数35天的日期
# print(money)
#
# r = redis.Redis(host='localhost',port=6379)  #r = redis.Redis(host='localhost',port=6379,password='810302')
# print(r.keys())
# stocks = ['601865.XSHG','600604.XSHG','002600.XSHE','000409.XSHE']  #   ,'000631.XSHE','000048.XSHE'

stocks = list(get_all_securities(['stock']).index) #股票池
#建立连接

# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')

for x in stocks:
    # dblist = client.list_database_names()
    stock_name = get_security_info(x).display_name
    is_ST = 'ST' in stock_name
    if(is_ST):
        continue
    df = get_price(x, start_date=sdate, end_date=edate, frequency='daily')
    df['rise'] = 100 * df['close'].pct_change().fillna(0) #计算涨幅，df是涨幅dataframe
    open = df['open'].iloc[-1] #开盘价
    high = df['high'].iloc[-1]
    low = df['low'].iloc[-1]
    close = df['close'].iloc[-1]
    volumn = df['money'].iloc[-1] / 100000000
    rise = df['rise'].iloc[-1] #今日涨幅
    ratio = get_ratio(df)  #均值回归系数
    db.origin.insert({'stock_id': x,
        'stock_name':stock_name,
        'open':open,
        'high': high,
        'low': low,
        'close': close,
        'volumn':volumn,
        'rise':rise,
        'lianban':cal_ban_num(x,sdate,edate),
        'ratio':ratio[0],
        'diff30':ratio[1],
        'date':edate,
        'start_date':get_security_info(x).start_date.strftime('%Y-%m-%d')
    })

# for item in col.find():
#     print (item)
#关闭连接
client.close()

