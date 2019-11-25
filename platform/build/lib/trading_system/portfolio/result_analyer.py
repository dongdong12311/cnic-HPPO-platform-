# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 09:56:14 2019

@author: Administrator
"""
import pandas as pd
import math
class Cal:
    def __init__(self):
        pass
    #计算每日收益率
    @staticmethod
    def _ratio(series):
        series_new = pd.Series([])
        for i in range(0, series.count() - 1):
            series_new[i] = (series[i + 1] - series[i]) / series[i] 
        return series_new
    # 均值
    @staticmethod
    def _mean(series):
        return series.mean()
    
    # 方差
    @staticmethod
    def _var(series):
        return series.var()
    
    
    # 年化收益率
    #最后一天资产净值^(250 / 天数) - 1
    @staticmethod
    def _annualized_returns( series, period = '1d' ):
        #period 表示我们序列的周期 默认为每一天
        if period == '1d':
            return series[series.last_valid_index()]**(250 / series.count()) - 1
        
    # beta  
    #series1 是投资组合净值  series2 是市场收益净值
    #组合收益率与市场收益率的协方差除以组合收益率的方差
    @staticmethod
    def _beta( series1, series2 ):
        series1_new = Cal._ratio(series1)
        series2_new = Cal._ratio(series2)
        return series2_new.cov(series1_new) / series2_new.var()
    
    #  alpha
    #组合年化收益率-市场年化收益率*beta
    @staticmethod
    def _alpha( series1, series2 ):
        return Cal._annualized_returns( series1, period = '1d' ) - Cal._annualized_returns( series2, period = '1d' ) * Cal._beta(series1, series2)
    
    # sharpe 夏普比率 series1 是投资组合净值  series2 是市场收益净值
    #每日收益率的平均值减无风险利率再除以每日收益率的标准差
    #假设无风险收益率为年化4%(国债)
    @staticmethod
    def _sharpe(series):
        series_new = Cal._ratio(series)
        if series_new.std():            
            return ((series_new.mean() - 0.00011) / series_new.std()) * math.sqrt(252)
        return None

    # 总收益率
    #最后一天资产净值 - 1
    @staticmethod
    def _total_returns(series):
        return series[series.last_valid_index()] - 1
       
    # downside_risk 最大回撤
    #回撤是资产在(0,T)的最高峰值与现在价值之间的回落值
    @staticmethod
    def _downside_risk(series):
        return (series.cummax() - series).max()
        
        

        