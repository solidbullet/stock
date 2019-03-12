#!/usr/bin/env python
# -*- coding:utf8 -*-
from jqdatasdk import *
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import time
import datetime

auth('13818571403','Jyq810302')

edate= datetime.datetime.strptime('2019-03-12',"%Y-%m-%d")
delta = datetime.timedelta(days=35)
n_days = edate - delta
sdate = n_days.strftime('%Y-%m-%d')
print(sdate)