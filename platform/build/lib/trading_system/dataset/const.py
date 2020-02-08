#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:09:24 2019

@author: dongdong
"""
base_path = "E:\\trading_data"
trading_calendar_path = "trading_calendar"
stock_index_path = "stock_index"
daily_data_path = "daily_data"
bcolz_data_path = "bcolz_data"

token = 'f867cf1c65e806c64096d26d7f7ea70db0c38bddb027c034f20c64de'
TRADE_DATE = 'date'
OPEN = 'open'
HIGH = 'high'
LOW = 'low'
CLOSE = 'close'
trade_data = 'trade_date'
pre_close = 'pre_close'
change = 'change'
pct_chg = 'pct_chg'
vol = 'vol'
amount = 'amount'
metas = (TRADE_DATE,OPEN,HIGH,LOW,CLOSE) 
trading_calendar_meta = (TRADE_DATE,)
stock_index_metas = (trade_data,CLOSE,OPEN,
                     HIGH,LOW,pre_close,change,pct_chg,vol,amount)
