#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:58:38 2019

@author: dongdong
"""

import bcolz
#from .tushare_market_data import LoadTradeCalendar,LoadHistoryData
from abc import ABCMeta, abstractmethod, abstractproperty
class DataSet(metaclass=ABCMeta):
    def __init__(self):
        pass
    @abstractmethod
    def Update(self,ind):
        pass
    
    @abstractmethod
    def GetLatestInd(self,N = 1):
        pass
    
    @abstractmethod
    def ComeToEnd(self,ind):
        pass   

    
class HistToryDataSet(DataSet):
    def __init__(self):
        self.data = None
    def init(self,start,end,data_path):
        self.ind_list = LoadTradeCalendar(start,end)
        self.data = bcolz.open(data_path)
        self.datasize = len(self.ind_list)

        
    def Update(self,ind):
        return ind + 1
    def ComeToEnd(self,ind):
        if ind >= self.datasize - 1:
            return True
        return False
    def GetLatestInd(self,N = 1):
        return self.ind_list[-1]   

    def now(self,ind):
        if ind >= len(self.ind_list):
            raise "error"
        return self.ind_list[ind]
    

    
    
    
class RealTimeDataSet(DataSet):
    def __init__(self):
        pass
    def Update(self,ind):
        self.data = self.GetNewData()
        return ind
    def ComeToEnd(self,ind):
        timenow = '15:00'
        if timenow:
            return False
def CreateHistoryDataSet():
    return HistToryDataSet()