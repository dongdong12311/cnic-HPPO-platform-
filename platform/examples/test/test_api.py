#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:53:16 2019

@author: dongdong
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:48:20 2019

@author: Administrator
"""

#from converter import StockBarConverter 
#from day_bar_store import DayBarStore
from trading_system.dataset.base_data_source import BaseDataSource
from trading_system.dataset.const  import base_path,bcolz_data_path
import os
import datetime
#a = DayBarStore("F:\\bcolz_data\\daily_data",StockBarConverter)
#s = a.get_bars("000001.SZ",['high'])
#temp = a.get_date_range("000001.SZ")

a = BaseDataSource(os.path.join(base_path,bcolz_data_path))
data = a.history_bars("000001.SZ",10,'1d','close',datetime.datetime(2019,6,1))
#s = a.stock_index_bars("000001.SH",10,'1d','close',datetime.datetime(2019,6,1))

temp = a.get_day_bars()[1]
m = temp.get_index()

#t = get_calendar()
#s = t.sessions_in_range(20160101,20160112)