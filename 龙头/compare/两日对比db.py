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

# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')

today = '2019-03-13'
tdate= datetime.datetime.strptime(today,"%Y-%m-%d")
delta = datetime.timedelta(days=1)  #取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
n_days = tdate - delta
yesterday = n_days.strftime('%Y-%m-%d')  #从今天往前面数1天的日期


dict_df = pd.DataFrame()
mycol = db['origin']
myquery = {"lianban": {"$gt": 0},"date":yesterday}
mydoc = mycol.find(myquery).sort("lianban",-1)
y_count = 0
num =3
for x in mydoc:
    stockid = x['stock_id']
    stockname = x['stock_name']
    lianban_num = x['lianban']
    ratio = round(x['ratio'],2)
    diff30 = round(x['diff30'],2)
    volumn = round(x['volumn'],2)
    rise = round(x['rise'], 2)
    condition = (lianban_num == num)
    if condition:
        y_count = y_count + 1
    query_rise = {"rise": {"$gt": 9}, "date": today, "stock_id":stockid}
    mydoc1 = mycol.find_one(query_rise)
    if mydoc1 and condition:
        dict1 = {'id': [stockid], 'name': [stockname], 'diff30':[diff30],'ratio':[ratio],'volumn':[volumn],'rise':[rise],'lianban': [lianban_num+1]}
        d = pd.DataFrame(dict1)
        dict_df = dict_df.append(d)
# for item in col.find():
t_count = len(dict_df)
ratio = 100*t_count/y_count
print("%d进%d:昨日连板 = %d个,今日连板 = %d个,成功率是:%.2f%%" %(num,num+1,y_count,t_count,ratio))
print (dict_df)
# dict_df.to_csv('c:\\stock\\20190312.csv')
#关闭连接
client.close()

