#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:41:39 2019

@author: dongdong
"""

import numpy as np
from trading_system.event.event import MarketEvent
class DataPtr:
    def __init__(self,base_data_source,ptrl_list):
        self._ind = 0
        self._base_data_source = base_data_source
        self._ptrl_list = ptrl_list
        self._end = len(ptrl_list)
    def get_trading_calendar(self,start,end):
        return self._base_data_source.get_trading_calendar(start,end)
    
    def latest_price(self,code,frequency):
        price_slice =  self._base_data_source.get_bar(code,self.now(),frequency)
        if price_slice is not None:
            return price_slice[4]
    def history_bars(self,code, expected_return_days, frequency,fields):
        return self._base_data_source.history_bars(code, expected_return_days,
                                                   frequency, fields, 
                                                   self.now(),
                     skip_suspended=False, include_now=False,
                     adjust_type='none', adjust_orig=None)
    def stock_index_bars(self,code,bar_count,frequency,fields,dt):
        return self._base_data_source.stock_index_bars(code,bar_count,frequency,fields,dt)
        
        
    def Update(self,events):

        if self._ind >= self._end - 1:
            return False
        self._ind =  self._ind + 1
        
        events.put(MarketEvent())
        return True

    def now(self):
        return self._ptrl_list[self._ind]
def CreateDataPtr(dataset,ptrl_list):
    return DataPtr(dataset,ptrl_list)