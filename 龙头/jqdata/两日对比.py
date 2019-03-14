from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
auth('13818571403','Jyq810302')

df = pd.read_csv("c:\\20190307.csv",encoding="ANSI")
five = df[df['连板'] == 5]
four = df[df['连板'] == 4]
three = df[df['连板'] == 3]
two = df[df['连板'] == 2]
one = df[df['连板'] == 1]

today = '2019-03-08'
lastdate = '2019-03-07'

dict = {}
dict_df = pd.DataFrame(dict)
for x in two['id']:
    p = get_price(x, start_date=today, end_date=today, frequency='daily')
    yesterday = get_price(x, start_date=lastdate, end_date=lastdate, frequency='daily')
    p['id'] = x
    p['name'] = get_security_info(x).display_name
    p.insert(0,'yclose',yesterday['close'][0])
    p['rise'] = 100*(p['close'] - p['yclose'])/p['yclose']
    dict_df=dict_df.append(p)
t_ban = dict_df[dict_df["rise"] > 9]
y_count = len(dict_df)
t_count = len(t_ban)
ratio = 100*t_count/y_count
print("昨日连板 = %d个,今日连板 = %d个,成功率是:%.2f%%" %(y_count,t_count,ratio))
# print("昨日数量:d%  今日进阶:d%  成功率是:%.2f%%" % (y_count,t_count,ratio))
print(dict_df.sort_values(by = 'rise',ascending = False))