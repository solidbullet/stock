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


df = pd.read_csv("c:\\stock\\list\\long.csv",dtype=str,encoding="ANSI")

dict_df = pd.DataFrame()
for index, row in df.iterrows():
    stockid = normalize_code(row['id'].zfill(6))
    name = row['name']
    if stockid.startswith('300'):
        continue
    myquery = {"date": edate, 'stock_id': stockid}
    mydoc = mycol.find_one(myquery)

    vibration = mydoc['vibration']
    reback = mydoc['reback']
    diff30 = mydoc['diff30']
    volumn = mydoc['volumn']
    rise = mydoc['rise']
    dict1 = {'id': [stockid], 'name': [name], 'diff30': [diff30], 'volumn': [volumn], 'reback': [reback],'vibration': [vibration]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)

reback = dict_df.sort_values(by = 'reback',ascending = False)[0:80]
vibration = dict_df.sort_values(by = 'vibration',ascending = False)[0:80]
result = pd.merge(reback,vibration).sort_values(by = 'vibration',ascending = False)
print(result)



