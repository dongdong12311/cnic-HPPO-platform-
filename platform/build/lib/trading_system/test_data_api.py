# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:48:20 2019

@author: Administrator
"""

#from converter import StockBarConverter 
#from day_bar_store import DayBarStore
from dataset.base_data_source import BaseDataSource
from dataset.const  import base_path,bcolz_data_path
import os
import datetime
#a = DayBarStore("F:\\bcolz_data\\daily_data",StockBarConverter)
#s = a.get_bars("000001.SZ",['high'])
#temp = a.get_date_range("000001.SZ")

a = BaseDataSource(os.path.join(base_path,bcolz_data_path))
#s = a.history_bars("000001.SZ",10,'1d','close',datetime.datetime(2019,6,1))
s = a.stock_index_bars("000001.SH",10,'1d','close',datetime.datetime(2019,6,1))

from api.api import get_calendar


t = get_calendar()
t.sessions_in_range(20160101,20160112)