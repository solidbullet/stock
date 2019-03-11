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


stock = '603729.XSHG'
sdate = '2019-03-08'
edate = '2019-03-08'

# print(money)
#
# r = redis.Redis(host='localhost',port=6379)  #r = redis.Redis(host='localhost',port=6379,password='810302')
# print(r.keys())
stocks = ['601865.XSHG','600604.XSHG','002600.XSHE','000409.XSHE','000631.XSHE','000048.XSHE']
#建立连接
client=MongoClient("hiiboy.com",27017)
#数据库名admin
db=client.stock
#认证用户密码
db.authenticate('jyq','123456')

for x in stocks:
    # dblist = client.list_database_names()
    df = get_price(x, start_date=sdate, end_date=edate, frequency='daily')
    open = df['open'].iloc[-1]
    high = df['high'].iloc[-1]
    low = df['low'].iloc[-1]
    close = df['close'].iloc[-1]
    volumn = df['money'].iloc[-1] / 100000000

    db.origin.insert({'stock_id': x,
        'stock_name':get_security_info(x).display_name,
        'rates':[open,high,low,close,volumn],
        'date':sdate
    })

# for item in col.find():
#     print (item)
#关闭连接
client.close()

