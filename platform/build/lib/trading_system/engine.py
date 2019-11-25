# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 21:47:27 2019

@author: Administrator
"""

from .api.api import CreateExcutionAPI,CreateMarketDataAPI,CreateOrderInfoAPI,CreatePositionInfoAPI,User_API,create_balanced_dates
from .event.event import CreateEventQueue
from .strategy.strategy import CreateStragety
from .excutor.excutor import CreateExcutor
from .dataset.dataptr import CreateDataPtr
from .dataset.dataset import CreateHistoryDataSet
from .portfolio.portfolio import CreateSimulatePortfolio
class Context:
    def __init__(self,config):
        names = self.__dict__
        for key in config.keys():
            names[key] = config[key]
        names['balance_dates'] = create_balanced_dates(
        config['start'],
        config['end'],
        {"dt":config['balanced_dates']['param']},
        method =config['balanced_dates']['method'])

class Handler():
    def __init__(self,events):
        self.events = events
        
    
class Engine:
    def __init__(self,analyser,config):
        self._analyser = analyser
        self.config = config
    def init(self,dataptr):
        trade_date = dataptr.now()
        self.initial_benchmark = dataptr.stock_index_bars(self.config['benchmark'],1,'1d','close',trade_date)[0]
        
    def __UpdateSimulatedData(self,events,dataptr,portfolio):
        if  dataptr.Update(events):
            portfolio.UpdatePositions(dataptr)
            return True
        return False
        
    def __UpdateRealData(self,events,dataptr):
        return  False
    
    def _Update(self,events,dataptr, portfolio = None):
        if self.__UpdateSimulatedData(events,dataptr,portfolio):
            self._Append_benchmark(dataptr)
            return True
        return False
    def _Append_benchmark(self,dataptr):
        trade_date = dataptr.now()
        cash = 0 
        market_value = dataptr.stock_index_bars(self.config['benchmark'],1,'1d','close',trade_date)[0]
        static_unit_net_value = market_value/self.initial_benchmark
        market_value = self.config['initial_capital'] * static_unit_net_value
        self._analyser.append_benchmark_portfolio(trade_date,
                                   cash,
                                   market_value,
                                   static_unit_net_value,
                                   market_value,
                                   static_unit_net_value,
                                   self.config['initial_capital'])          
            
    def Run(self,init,handle_bar,api,excutor,dataptr,portfolio = None):  
        context = Context(self.config)
        init(context)
        
        events = CreateEventQueue()
        api.RegisterEvents(events)
        while 1:
            res =  self._Update(events,dataptr,portfolio)
            if not res:
                return portfolio.get_log()
            while 1:
                # 获取待处理的事件，如果队列空就结束循环
                if  events.qsize() == 0:
                    break
                else:
                    event = events.get(False)
                # 计算信号    
                if event.type == 'MARKET':
                    handle_bar(context,api)
                # 执行订单
                elif event.type =='ORDER':   
                    excutor.execute_order(event)
                    
                elif event.type =='CHANGE_WEIGHT':   
                    excutor.order_target_percent(event)
                else:
                    raise TypeError    
from trading_system.dataset.base_data_source import BaseDataSource
from trading_system.analyser.analyser import Analyser
import os
from .dataset.const import base_path,bcolz_data_path

def Run_func(init,handle_bar,config):                    
    start = config['start']
    end = config['end']      
    datapath = os.path.join(base_path,bcolz_data_path)         
    dataset = BaseDataSource(datapath)
    ptrl_list = dataset.get_trading_calendar(start,end)
    analyser = Analyser()
    # _______________dataset_______________   
    dataptr = CreateDataPtr(dataset,ptrl_list)
    # ____________portfolio________________
    portfolio = CreateSimulatePortfolio(analyser,
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
    
    #_____________excutor_______________
    excutor = CreateExcutor()
    excutor.RegisterAPI(excution_API)
            
    # ____________engine________________
    engine = Engine(analyser,config)
    engine.init(dataptr)
    from trading_system.portfolio.summarise import summarise
    return summarise(engine.Run(init,handle_bar,api,excutor,dataptr,portfolio),config)
    