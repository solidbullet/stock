#!/usr/bin/env python
# -*- coding:utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt
import math
# data= pd.read_csv("c:\\stock\\2019-03-19ratio.csv",encoding='utf-8')
# data = data.sort_values(by = 'rise',ascending = False)
# rise = data['rise']
# print(rise)
# plt.hist(rise)
# plt.show()


client=MongoClient("localhost",27017)
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')

date = "2019-03-21"
mycol = db['origin']
myquery = {"date":date}
mydoc = mycol.find(myquery).sort("rise",-1)
arr_rise = []
arr_ratio = []
arr_volumn = []
for x in mydoc:
    ratio = x['ratio']
    rise = x['rise']
    volumn = x['volumn']
    if math.isnan(0 * float(ratio)):  # 把inf值转化为nan，再进行判断
        continue
    arr_ratio.append(ratio)
    arr_rise.append(rise)
    arr_volumn.append(volumn)

plt.figure(date,figsize=(16,8),dpi=80)  # 置一块自定义大小的画布，使得后面的图形输出在这块规定了大小的画布上，其中参数figsize设置画布大小
# plt.figure('hello') #图像标题
plt.subplot(221)
plt.title('ratio')
plt.hist(arr_ratio)

plt.subplot(222)
plt.title('rise')
plt.hist(arr_rise)

plt.subplot(223)
plt.title('volumn')
plt.hist(arr_volumn)
plt.show()