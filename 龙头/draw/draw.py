#!/usr/bin/env python
# -*- coding:utf8 -*-
from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt
import ch
ch.set_ch()
import matplotlib.dates as mdate

auth('13818571403','Jyq810302')



# stock = '603729.XSHG'
edate = '2019-03-15'


# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')


dict_df = pd.DataFrame()

mycol = db['origin']

i = 8
while i > 0:
    i = i - 1
    tdate = datetime.datetime.strptime(edate, "%Y-%m-%d")
    delta = datetime.timedelta(days=i)  # 取35天的数据，不然均值回归不准，均值回归是按照现价与MA30的差值计算的
    n_days = tdate - delta
    sdate = n_days.strftime('%Y-%m-%d')  # 从今天往前面数35天的日期

    set_date = datetime.datetime.strptime(sdate, "%Y-%m-%d")
    weekday = set_date.weekday()
    is_week = weekday in [5,6]


    if is_week:
        continue
    myquery = {"rise": {"$gt": 9}, "date": sdate}
    count = mycol.find(myquery).count()  # .sort("lianban",-1)
    dict1 = {'count': [count], 'date': [set_date]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)

    # print("date:%s,次数:%d"%(sdate,count))
dragon = dict_df.sort_values(by='date', ascending=True)
dragon = dragon .set_index('date')
print(dragon)

plt.figure(1)   #创建图表1
# plt.subplot(212)
plt.ylabel('涨停数量')
# fig = plt.figure(figsize=(10,6))
# ax = fig.add_subplot(1,1,1)
# plt.xaxis.set_major_formatter(mdate.DateFormatter('%b %Y'))
# plt.plot(dragon)

plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdate.DayLocator())
dragon['count'].plot(figsize=(15,8))
plt.gcf().autofmt_xdate()

plt.show()

rest_holiday=[
    '2018-12-31',
    '2019-01-01','2019-02-04','2019-02-05','2019-02-06','2019-02-07','2019-02-08',
    '2019-04-05','2019-04-29','2019-04-30','2019-05-01','2019-06-07','2019-09-13',
    '2019-10-01','2019-10-02','2019-10-03','2019-10-04','2019-10-07','2019-12-30',
    '2019-12-31',
    '2020-01-01','2020-01-24','2020-01-27','2020-01-28','2020-01-29','2020-01-30',
    '2020-04-06','2020-05-01','2020-06-25','2020-06-26','2020-10-01','2020-10-02',
    '2020-10-05','2020-10-06','2020-10-07','2020-10-08',
    '2021-01-01',
]
#把调休的工作日加到这里面
rest_workday=[
    '2019-02-02','2019-02-03','2019-04-27','2019-02-28','2019-09-29','2019-10-12',
    '2019-12-28','2019-12-29',
    '2020-01-19','2020-02-01','2020-06-28','2020-09-27','2020-10-10',
]

# def is_holiday(start_date,end_date):
#     set_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
#     for i in range(10000):
#         set_date_str=set_date.strftime('%Y-%m-%d')
#         if set_date_str>=end_date:
#             break
#         #0~6代表周一~周日
#         weekday=set_date.weekday()
#         if set_date_str in rest_holiday or (weekday in [5,6] and set_date_str not in rest_workday):
#             is_holiday=1
#             is_monday=0
#         else:
#             is_holiday = 0
#             is_monday = 1
#         #日期加1
#         set_date = set_date + datetime.timedelta(days=1)

start_date='2019-04-06'
end_date='2021-01-01'
set_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
set_date_str=set_date.strftime('%Y-%m-%d')
weekday=set_date.weekday()
# print(weekday in [5,6])
# is_holiday(start_date,end_date)

#关闭连接
client.close()

