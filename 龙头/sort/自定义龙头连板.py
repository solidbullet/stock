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



# stock = '603729.XSHG'
edate = '2019-03-13'
tdate= datetime.datetime.strptime(edate,"%Y-%m-%d")
delta = datetime.timedelta(days=1)  #取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
n_days = tdate - delta
sdate = n_days.strftime('%Y-%m-%d')  #从今天往前面数35天的日期

# stocks = ['601865.XSHG','600604.XSHG','002600.XSHE','000409.XSHE']  #   ,'000631.XSHE','000048.XSHE'

stocks = list(get_all_securities(['stock']).index) #股票池
#建立连接

# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')
mycol = db['dragon']
mydoc = mycol.find({})
dict_df = pd.DataFrame()
for x in mydoc:
    stockid = x['stock_id']
    df = get_price(stockid, start_date=sdate, end_date=edate, frequency='daily')
    # print(stockid)
    df['rise'] = 100 * df['close'].pct_change().fillna(0)  # 计算涨幅，df是涨幅dataframe
    rise = df['rise'].iloc[-1]  # 今日涨幅

    myquery = {'stock_id': stockid}
    newvalues = {"$set": {'lianban':cal_ban_num(stockid,sdate,edate),'rise':rise}}

    mycol.update_one(myquery, newvalues)
    # x['rise'] = rise
    # print(x['stock_id'])

for x in mycol.find({},{'_id':0}).sort("rise",-1):
  print(x)
#关闭连接
client.close()

