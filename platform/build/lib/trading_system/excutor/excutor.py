#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:37:13 2019

@author: dongdong
"""

class Excutor:
    def __init__(self):
        pass
    def RegisterAPI(self,excution_API):
        self._excution_API = excution_API
    def execute_order(self,orderevent):
        self._excution_API.execute_order(orderevent)
    def order_target_percent(self,event):
        symbols = event.symbols
        prices = event.prices
        weights = event.weights
        ordertime = event.ordertime
        self._excution_API.order_target_percent(symbols,weights,prices,ordertime)
def CreateExcutor():
    return Excutor()