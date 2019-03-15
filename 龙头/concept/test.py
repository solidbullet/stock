#!/usr/bin/env python
# -*- coding:utf8 -*-
from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime
from pymongo import MongoClient
auth('13818571403','Jyq810302')



stock = '603729.XSHG'
edate = '2019-03-14'

q = query( valuation).filter(valuation.code == stock)
df_market = get_fundamentals(q, edate)
market = df_market['market_cap'][0]
print(market)



