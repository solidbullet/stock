from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
auth('13818571403','Jyq810302')

def cal_ban_num( stock,begindate,enddate ):
    df = get_price(stock, start_date=begindate, end_date=enddate, frequency='daily')
    df['rise'] = df['close'].pct_change().fillna(0)
    i = 0
    while i < len(df):
        #print(df['rise'][len(df) - i - 1])
        i += 1
        if df['rise'][len(df) - i - 1] < 0.099:
            break
    return i

#stock = '601519.XSHG'
sdate = '2019-02-01'
edate = '2019-02-27'
#print(cal_ban_num(stock,sdate,edate))
dict = {'id':['000000.XXXX'],'count':[0]}
dict_df = pd.DataFrame(dict)
stocks = list(get_all_securities(['stock']).index)
#stocks = ['601519.XSHG','600604.XSHG','600009.XSHG']
for x in stocks:
    #print(x)
    dict1 = {'id':x,'count':[cal_ban_num(x,sdate,edate)]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)
dragon = dict_df[dict_df['count'] > 1].sort_values(by = 'count',ascending = False).iloc[0:30]
print(dragon)