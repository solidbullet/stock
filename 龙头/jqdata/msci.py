from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from pymongo import MongoClient
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
auth('13818571403','Jyq810302')


sdate = '2019-03-13'
edate = '2019-03-14'

# client=MongoClient("hiiboy.com",27017)
client=MongoClient("localhost",27017)
#数据库名admin
db=client.stock
#认证用户密码
# db.authenticate('jyq','123456')
mycol = db['origin']

stocks = get_concept_stocks('GN240')

dict_df = pd.DataFrame()

# 通过数据库查询
for x in stocks:
    myquery = {"stock_id": x, "date": edate}
    mydoc = mycol.find_one(myquery,{'_id':0,'rise':1,'ratio':1,'diff30':1,'lianban':1,'volumn':1,'stock_name':1,'stock_id':1})
    # id = mydoc['stock_id']
    if mydoc:
        rise = round(mydoc['rise'],2)
        ratio = round(mydoc['ratio'],2)
        diff30 = round(mydoc['diff30'],2)
        volumn = round(mydoc['volumn'],2)
        lianban = mydoc['lianban']
        name = mydoc['stock_name']
        dict1 = {'id':[x],'name':[name],'diff30':[diff30],'ratio':[ratio],'volumn':[volumn],'lianban':[lianban],'rise':[rise]}
        d = pd.DataFrame(dict1)
        dict_df = dict_df.append(d)
dragon = dict_df.sort_values(by = 'rise',ascending = False)
print(dragon)