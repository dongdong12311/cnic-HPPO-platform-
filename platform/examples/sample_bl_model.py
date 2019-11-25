# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:47:51 2019

@author: dongdong
"""


import numpy as np
'this example is given to realize the cvar model '
from trading_system.api.api import describe,draw_efficient_frontier,get_BL_efficient_frontier,get_BL_minimum_variance_portfolio,get_BL_maximum_utility_portfolio,get_maximum_sharpe_portfolio
from trading_system.api.api import create_balanced_dates
import pandas as pd




def initialize(context):
    pass

    
    
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
        df = pd.DataFrame(temp)
        #计算收益率数据
        for index in context.stocks:
            df[index] = df[index] / df[index].shift() - 1.
        return_table = df.dropna()
        output=describe(return_table, is_print=True) 
        covariance_matrix = output['covariance_matrix']
        tau = 0.05
        # - 生成观点矩阵P、Q、Omega，根据我们对股市资产配置的未来走势的判断，给出下面3个观点：
        # - 观点1： 000004.SZ的收益低于000005.SZ收益2%
        ## - 观点2： '000006.SZ'收益上调到10%，
        ## - 观点3：'000007.SZ'收益5% 

        P = np.array([[0,0,1,-1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]])
        Q = np.array([0.02,0.1,0.05])
        
        Omega = tau*(P.dot(covariance_matrix).dot(P.transpose()))
        
        Omega = np.diag(np.diag(Omega,k=0))
        
        weights=get_BL_minimum_variance_portfolio(return_table,tau=0.05,P=P,Q=Q,Omega=Omega, allow_short=False, show_details=True)
        
        weight = []
        prices = []
        for code in context.stocks:
            weight.append(weights[code])
            prices.append(data.latest_price(code,"1d"))
        data.order_target_percent(context.stocks, weight,prices)  