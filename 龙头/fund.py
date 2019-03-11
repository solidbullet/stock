from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
auth('13818571403','Jyq810302')

d2 = datetime.date.today()
fiance = get_industry_stocks('HY493', date=d2) #j聚宽一级金融
money = get_money_flow(fiance, '2019-03-01', '2019-03-01')
print(money.sum())
print(fiance)