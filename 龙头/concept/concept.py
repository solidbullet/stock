from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
auth('13818571403','Jyq810302')



def cal_ban_num( stock,begindate,enddate ):
    df = get_price(stock, start_date=begindate, end_date=enddate, frequency='daily')
    df['rise'] = df['close'].pct_change().fillna(0)
    i = 0
    while i < len(df):
        #print(df['rise'][len(df) - i - 1])

        if df['rise'][len(df) - i - 1] < 0.09:
            break
        i += 1
    return i

#stock = '601519.XSHG'
sdate = '2019-02-20'
edate = '2019-03-12'
#print(cal_ban_num(stock,sdate,edate))
dict = {'id':['000000.XXXX'],'name':['YYYY'],'lianban':[0]}
dict_df = pd.DataFrame(dict)
# stocks = list(get_all_securities(['stock']).index)
stocks = get_concept_stocks('GN028')
#stocks = ['601865.XSHG','600604.XSHG','002600.XSHE']
for x in stocks:
    #print(x)
    d1 = get_security_info(x).start_date
    d2 = datetime.date.today()
    if (d2-d1).days < 20:
        continue
    #hangye = get_industry(x,date=d2)
    #industry = hangye[x]['zjw']['industry_name']
    dict1 = {'id':x,'name':[get_security_info(x).display_name],'lianban':[cal_ban_num(x,sdate,edate)]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)
dragon = dict_df[dict_df['lianban'] >= 1].sort_values(by = 'lianban',ascending = False) #.iloc[0:100]
# dragon.to_csv('c:\\stock\\20190308.csv')
sum = len(stocks)
t_count = len(dragon)
ratio = 100*t_count/sum
print("2019年3月12日智能电网概念：总共股票数量=%d个,今日涨停 = %d个,成功率是:%.2f%%" %(sum,t_count,ratio))
print(dragon)