#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:57:23 2019

@author: dongdong
"""


from trading_system.api.api import create_balanced_dates
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

def initialize(context):
    pass
    
import pandas as pd
def handle_data(context, data):
    date = data.today()
    if date in context.balance_dates:
        temp = {}
        for code in context.stocks:
            history_price = data.history_bars(code,
                                              context.expected_return_days,
                                              '1d','close')
            if history_price is not None:     
                temp.update({code:history_price})
        history_prices = pd.DataFrame(temp)
        mu = expected_returns.mean_historical_return(history_prices)
        if context.cov_method == 'sample':
            S = risk_models.sample_cov(history_prices)
        elif context.cov_method == 'semi':
            S = risk_models.semicovariance(history_prices)
        elif context.cov_method == 'exp_cov':
            S = risk_models.exp_cov(history_prices)
            
        ef = EfficientFrontier(mu, S)
        
        if context.opt_criterion == 'max_sharpe':
            weights = ef.max_sharpe()
        elif context.opt_criterion == 'efficient_return':
            weights = ef.efficient_return(context.target_return)
        elif context.opt_criterion == 'efficient_risk':
            weights = ef.efficient_risk(context.targe_risk, context.risk_free_rate)
        elif context.opt_criterion == 'min_volatility':
            weights = ef.min_volatility()
        
        if context.cleaned_weights is True:
            weights = ef.clean_weights()
        
        weight = []
        prices = []
        for code in context.stocks:
            weight.append(weights[code])
            prices.append(data.latest_price(code,"1d"))
        
        data.order_target_percent(context.stocks, weight,prices)    
    
    
    
    