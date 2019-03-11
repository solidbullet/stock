from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
auth('13818571403','Jyq810302')

stock = '601519.XSHG'
sdate = '2019-03-07'
edate = '2019-03-08'

#stocks = list(get_all_securities(['stock']).index)
#stocks = ['601865.XSHG','600604.XSHG','002600.XSHE','000409.XSHE','000631.XSHE','000048.XSHE']

df = pd.read_csv("c:\\stock\\devil.csv",encoding="ANSI")
stocks =  df['id']


dict = {'id':['000000.XXXX'],'name':['YYYY'],'rise':[-100]}
dict_df = pd.DataFrame(dict)

for x in stocks:

    name = get_security_info(x).display_name
    is_ST = 'ST' in name
    if(is_ST):
        continue
    df = get_price(x, start_date=sdate, end_date=edate, frequency='daily')
    df['rise'] = 100 * df['close'].pct_change().fillna(0)
    #print(df)
    rise = df['rise'].iloc[-1]
    dict1 = {'id':x,'name':[get_security_info(x).display_name],'rise':[rise]}
    d = pd.DataFrame(dict1)
    dict_df = dict_df.append(d)
dragon = dict_df.sort_values(by = 'rise',ascending = False)
print(dragon)
