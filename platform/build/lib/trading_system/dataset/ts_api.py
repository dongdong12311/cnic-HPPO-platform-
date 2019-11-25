#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:20:56 2019

@author: dongdong
"""
from const import *
import tushare as ts
ts.set_token(token)
pro = ts.pro_api()
def GetStockList():
    global pro
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return data['ts_code']