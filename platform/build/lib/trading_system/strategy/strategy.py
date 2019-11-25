#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:31:56 2019

@author: dongdong
"""
from abc import abstractmethod
from trading_system.event.event import OrderEvent
class Strategy:
    def __init__(self):
        pass
    @abstractmethod
    def calculate_signals(self):
        raise "no implement error"
    
    def ConnectToEventQueue(self,events):
        self.events = events 
        
    def GenerateBuyOrder(self,code,size,price):
        self.events.put(OrderEvent(code,1,size,price,'B'))
         
    def GenerateSellOrder(self,code,size,price):
        self.events.put(OrderEvent(code,1,size,price,'S'))
        
    def RegisterAPI(self,market_data_API,position_info_API,order_info_API):
        self._market_data_API = market_data_API
        self._position_info_API = position_info_API
        self._order_info_API = order_info_API
        


    
class MyStrategy(Strategy):
    def __init__(self):
        pass

    def calculate_signals(self):
        code = '600232.SH'
        price = 1.0
        size = 100
        data = self._market_data_API.GetSliceData(3)
        print(data)
        self.GenerateBuyOrder(code,size,price)
        positions = self._position_info_API.GetPosition(code)
        if positions:
            self.GenerateSellOrder(code,size,price)
        

def CreateStragety():
    return MyStrategy()