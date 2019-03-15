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


# stocks = list(get_all_securities(['stock']).index) #股票池
#建立连接
df = pd.read_csv("c:\\stock\long.csv",dtype=str)  #  ,encoding="ANSI"


# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')


for index, row in df.iterrows():
    db.dragon.insert({'stock_id': normalize_code(row['id']),
        'stock_name':row['name'],
        'sort':row['sort'],
        'concept':row['concept']
    })

# for item in col.find():
#     print (item)
#关闭连接
client.close()

