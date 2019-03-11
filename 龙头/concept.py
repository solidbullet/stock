from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
auth('13818571403','Jyq810302')

df = pd.read_csv("c:\\20190305.csv",encoding="ANSI")
four = df[df['连板'] == 4]
three = df[df['连板'] == 3]
two = df[df['连板'] == 2]
one = df[df['连板'] == 1]

today = '2019-03-06'
lastdate = '2019-03-05'

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
print(dict_df.sort_values(by = 'rise',ascending = False))