# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 22:23:38 2019

@author: Administrator
"""
import datetime
from .result_analyer import Cal
def int_to_datetime(data):
    year = int(data / 10000)
    day = data % 100
    month = int(data/100) %100
    return    (year,month,day)
def summarise(res,config):
    portfolio_series = res['sys_analyser']['portfolio']['static_unit_net_value']
    market_series = res['sys_analyser']['benchmark_portfolio']['static_unit_net_value']
    calculator = Cal()
    alpha = calculator._alpha(portfolio_series,market_series)
    annualized_returns = calculator._annualized_returns(portfolio_series)
    benchmark_annualized_returns = calculator._annualized_returns(market_series)
    benchmark_total_returns = calculator._total_returns(market_series)
    max_drawdown = calculator._downside_risk(portfolio_series)
    beta = calculator._beta(portfolio_series,market_series)
    sharpe = calculator._sharpe(portfolio_series)
    total_returns = calculator._total_returns(portfolio_series)
    volatility = calculator._var(portfolio_series)
    start = config['start']
    (year,month,day) = int_to_datetime(start)
    start_datetime = datetime.datetime(year,month,day)
    end = config['end']
    (year,month,day) = int_to_datetime(end)
    end_datetime = datetime.datetime(year,month,day) 
    summary = {
               'STOCK':config['initial_capital'],
               'alpha':alpha,
               'annualized_returns':annualized_returns,
               'benchmark_annualized_returns':benchmark_annualized_returns,
               'benchmark_total_returns':benchmark_total_returns,
               'beta':beta,
               'cash':config['initial_capital'],
               'downside_risk':0.0,
               'end_date':end_datetime,
               'information_ratio':0.0,
               'max_drawdown':max_drawdown,
               'run_type':'0',
               'sharpe':sharpe,
               'sortino':0.0,
                'start_date':start_datetime,
                'strategy_file':'name',
                'strategy_name':'name',
                'total_returns':total_returns,
                'total_value':total_returns,
                'tracking_error':'0',
                'unit_net_value':1.0,
                'units':1.0,
                'volatility':volatility
            }
    res['sys_analyser']['summary'] = summary       
    return res