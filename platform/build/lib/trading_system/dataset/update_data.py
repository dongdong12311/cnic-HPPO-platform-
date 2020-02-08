#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:49:27 2019

@author: dongdong
"""

'update data'
from .const import *
import numpy as np
import pandas as pd
from .ts_api import pro
from .tushare_market_data import LoadTsTradeCalendar
from dateutil.parser import parse
def GetLatestMeta(data,meta):
    if len(data[meta]):    
        date = data[meta][-1:].values[0]
    else:
        date = ''
    return date
    
def Update_daily_trading_calendar(file_path):

    global pro
    data = pd.read_csv(file_path,dtype = {TRADE_DATE:str})
    latest_date = GetLatestMeta(data,TRADE_DATE)
    temp = LoadTsTradeCalendar(latest_date,'')[1:]
    for i in range(len(temp)):
        temp_time = temp[i]
        temp[i] = np.uint32(temp_time.year * 10000 + temp_time.month * 100 + temp_time.day)
    df = pd.DataFrame(temp,columns = [TRADE_DATE])
    
    res = pd.concat([data,df],axis=0,ignore_index=True)
    res.to_csv(file_path,index = False,columns = [TRADE_DATE])

    return 
def Update(file_paths,code):
    global pro
    data = pd.read_csv(file_paths,dtype = {TRADE_DATE:str})
    date = GetLatestMeta(data,TRADE_DATE)
    try:    
        df = pro.query('daily', ts_code=code, start_date=date, end_date='')
    except Exception as e:
        print(e)
        return 
        
    'drop start date'
    df.insert(0,TRADE_DATE,df['trade_date'])
    df = df.drop(len(df[TRADE_DATE])-1)
    df = df.sort_values(by=TRADE_DATE)
    
    print('update' + code + 'from' + df[TRADE_DATE][0] + 'to'+ df[TRADE_DATE][-1:] )
    'contact two csv file'
    listed_meta = list(metas)
    res = pd.concat([data,df[listed_meta]],axis=0,ignore_index=True)
    res.to_csv(file_paths,index = False,columns = listed_meta)
    
def update_stock_index(file_path):
    import os
    try:
        os.mkdir(file_path)
    except:
        pass
    global pro
    index_dic = {
        'MSCI':'MSCI指数',
        'CSI':'中证指数',
        'SSE':'上交所指数',
        'SZSE':'深交所指数',
        'CICC':'中金所指数',
        'SW':'申万指数',
        'OTH':'其他指数'
    }
    for key in index_dic.keys():
        "this should be removed "
        #if key == 'SSE':
            #pro = ts.pro_api()
        df = pro.index_basic(market= key )
        for code in df['ts_code']:
            "this should be removed "
            if code == '000001.SH' or code == '000300.SH':
                data = pro.index_daily(ts_code=code)
                data = data.sort_values(by = 'trade_date')
                data = data.drop(['ts_code'],axis=1)
                data.to_csv(os.path.join(file_path,code),index = False)
        
