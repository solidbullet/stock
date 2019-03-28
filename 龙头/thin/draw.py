import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
import matplotlib.pyplot as plt
import pylab as mpl  #导入中文字体，避免显示乱码
import matplotlib.dates as mdate

mpl.rcParams['font.sans-serif']=['SimHei']  #设置为黑体字

dateparse = lambda dates:pd.datetime.strptime(dates,'%Y/%m/%d')
data= pd.read_csv("c:\\stock\\thin.csv",encoding='utf-8',parse_dates=['date'],date_parser=dateparse)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y/%m/%d'))
diff = data['weight'].iloc[0]-data['weight'].iloc[-1]
title = '江远强体重曲线[2019年]     总偏差:'+ str(round(diff,2)) + '公斤'

plt.title(title)
plt.ylabel('体重(千克)')
plt.xticks(rotation=45)
ax.plot(data['date'],data['weight'],color='R')
plt.show()