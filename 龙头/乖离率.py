from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)
auth('13818571403','Jyq810302')

def get_ratio(str_code,sdate,edate):
    df = pd.DataFrame()
    df = df.append(get_price(str_code, start_date=sdate, end_date=edate, frequency='daily'))

    if df.empty:
        return 0
    b = df.sort_index(axis = 0,ascending = True)
    r = b.rolling(window = 30,min_periods = 1)
    ma30 = r['close'].aggregate(np.mean)
    std = r['close'].aggregate(np.std)
    #var = r['close'].aggregate(np.var)
    b['ma30'] = ma30
    b['std'] = std
    b['ratio'] = (b['close'] - b['ma30']) /b['std']
    #print(b.tail())
    return b.iloc[-1]['ratio']

stock = '601519.XSHG'
sdate = '2019-01-01'
edate = '2019-03-06'

stocks = list(get_all_securities(['stock']).index)
dfratio = pd.DataFrame(index = np.arange(len(stocks)),columns=['ratio','id','name'])
i = 0
for x in stocks:
    dfratio['ratio'][i] = get_ratio(x,sdate,edate)
    dfratio['id'][i] = x
    dfratio['name'][i] = get_security_info(x).display_name
    i = i+1
    #print(i, sz50['code'].iloc[i])
print(dfratio.sort_values(by = 'ratio'))