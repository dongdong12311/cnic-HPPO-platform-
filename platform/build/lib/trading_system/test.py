# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 13:48:20 2019

@author: Administrator
"""

from dataset.converter import StockBarConverter 
from dataset.day_bar_store import DayBarStore
from dataset.base_data_source import BaseDataSource
import datetime
from dataset.const import base_path,bcolz_data_path
import os
#a = DayBarStore("F:\\bcolz_data\\daily_data",StockBarConverter)
#s = a.get_bars("000001.SZ",['high'])
#temp = a.get_date_range("000001.SZ")
from api.api import CreateExcutionAPI,CreateMarketDataAPI,CreateOrderInfoAPI,CreatePositionInfoAPI,User_API
from event.event import CreateEventQueue
from strategy.strategy import CreateStragety
from excutor.excutor import CreateExcutor
from dataset.dataptr import CreateDataPtr
from dataset.dataset import CreateHistoryDataSet
from portfolio.portfolio import CreateSimulatePortfolio
a = BaseDataSource(os.path.join(base_path,bcolz_data_path))
s = a.history_bars("000001.SZ",10,'1d','close',datetime.datetime(2019,5,30))
s = a.get_trading_calendar(20190102,20191211)
s = a.get_bar("000001.SZ",datetime.datetime(2019,5,30),"1d")

start = 20190102
end = 20191211       
print('init data')     
dataset = BaseDataSource(config['data_path'])
ptrl_list = dataset.get_trading_calendar(start,end)
print("done")
# _______________dataset_______________   
dataptr = CreateDataPtr(dataset,ptrl_list)
# ____________portfolio________________
portfolio = CreateSimulatePortfolio(
        config['initial_capital']) 
#_____________apply api________________
      
market_data_API = CreateMarketDataAPI()
market_data_API.RegisterDataPtr(dataptr)


position_info_API = CreatePositionInfoAPI()
position_info_API.RegisterPortfolio(portfolio)

'simulated trading do not need order info api'
#order_info_API = CreateOrderInfoAPI()


excution_API = CreateExcutionAPI()
excution_API.RegisterSimulatedPortfolio(portfolio)

api  = User_API(market_data_API,position_info_API)
temp = api.get_trading_calendar(start,end)