#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 13:30:08 2019

@author: dongdong
"""
from abc import abstractmethod
from scipy.stats.mstats import gmean
import numpy as np
from trading_system.event.event import OrderTargetPercentEvent
import datetime
import pandas as pd
class API:
    def __init__(self):
        pass
class MarketDataAPI(API):
    def __init__(self):
        pass
    def RegisterDataPtr(self,dataptr):
        self._dataptr = dataptr
    def latest_price(self,code,frequency):
        return self._dataptr.latest_price(code,frequency)
    def now(self):
        return self._dataptr.now()
    def history_bars(self,stock, expected_return_days, period,field):
        return self._dataptr.history_bars(stock, expected_return_days, period,field)

class SimulatedMarketDataAPI(MarketDataAPI):
    def __init__(self):
        super().__init__()
    
class PositionInfoAPI(API):
    def __init(self):
        super().__init__()
    def RegisterPortfolio(self,portfolio):
        self._portfolio = portfolio
    def GetPosition(self,code):
        return self._portfolio.GetPosition(code)
    def GetAvailableMoney(self):
        return self._portfolio.AvailableMoney()
class SimulatedPositionInfoAPI(PositionInfoAPI):
    def __init__(self):
        super().__init__()
        
        
class ExcutionAPI(API):
    def __init__(self):
        pass
    @abstractmethod
    def execute_order(self,orderevent):
        raise "no implement error"
        
class SimulatedExcutionAPI(ExcutionAPI):
    def __init__(self):
        super().__init__()
    def RegisterSimulatedPortfolio(self,portfolio):
        self.__portfolio = portfolio
    def execute_order(self,orderevent):
        symbol = orderevent.symbol
        order_type = orderevent.order_type
        quantity = orderevent.quantity
        price = orderevent.price
        direction = orderevent.direction
        ordertime = 2018
        self.__portfolio.UpdatePosition(symbol,order_type,quantity,price,direction,ordertime)
    def order_target_percent(self,stock,weight,price,ordertime):
        #print(price)
        self.__portfolio.UpdatePortfolio(stock,weight,price,ordertime)
    
    
        
def CreateMarketDataAPI():
    return SimulatedMarketDataAPI()

def CreatePositionInfoAPI():
    return SimulatedPositionInfoAPI()

def CreateOrderInfoAPI():
    return None
def CreateExcutionAPI():
    return SimulatedExcutionAPI()

class get_calendar:
    def __init__(self):
        from trading_system.dataset.const  import base_path,bcolz_data_path,trading_calendar_path
        import os
        from trading_system.dataset.trading_dates_store import TradingDatesStore
        self._cal = TradingDatesStore(os.path.join(
                os.path.join(base_path,bcolz_data_path),trading_calendar_path))
    def sessions_in_range(self,start,end):
        return self._cal.get_trading_calendar(start,end)

class User_API:
    def __init__(self,market_data_api,position_info_api):
        self._market_data_api = market_data_api
        self._position_info_api = position_info_api
    def RegisterEvents(self,events):
        self._events = events
    def history_bars(self,stock, expected_return_days, period,field):
        return self._market_data_api.history_bars(stock, expected_return_days, period,field)
    def order_target_percent(self,stocks,weights,prices): 
        self._events.put(OrderTargetPercentEvent(stocks,weights,prices,self._market_data_api.now()))
        
    def GetPositionWeight(self,code):
        pass
    
    def Buy(self,code,price,size):
        pass
    
    def Sell(self,code,price,size):
        pass
    def get_trading_calendar(self,start,end):
        return self._market_data_api.get_trading_calendar()
    
    def latest_price(self,code,frequency):
        return self._market_data_api.latest_price(code,frequency)
    
    def PositionValue(self):
        pass
    
    def now(self):
        return self._market_data_api.now()
    
    def today(self):
        d = self.now()
        return datetime.date(d.year,d.month,d.day)
    
#建立函数计算年化收益率、年化标准差、相关系数矩阵

def describe(return_table, is_print=True):
    """
    输出收益率矩阵的描述性统计量，包括：
        年化收益率
        年化标准差
        相关系数矩阵
    
    Args:
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        is_print (bool): 是否直接输出

    Returns:
        dict: 描述性统计量字典，键为"annualized_return", "annualized_volatility", "covariance_matrix"和"coefficient_matrix"

    Examples:
        >> describe(return_table)
        >> describe(return_table, is_print=True)
    """
    
    output = {}
    output['annualized_return'] = pd.DataFrame(dict(zip(return_table.columns, gmean(return_table+1.)**252 - 1.)), index=[0], columns=return_table.columns)
    output['annualized_volatility'] = pd.DataFrame(return_table.std() * np.sqrt(250)).T
    output['covariance_matrix'] = return_table.cov() * 250.
    output['coefficient_matrix'] = return_table.corr()
        
    if is_print:
        for key, val in output.items():
            print("{}:\n{}\n".format(key, val))
    
    return output

from cvxopt import matrix, solvers


# 计算最小方差组合
def get_BL_minimum_variance_portfolio(return_table,tau=0.05,P=None,Q=None,Omega=None, allow_short=False, show_details=True):
    """
    计算最小方差组合
    
    Args:
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        allow_short (bool): 是否允许卖空3
        show_details (bool): 是否显示细节
        P(np.array): 观点矩阵
        Q(np.array): 观点收益矩阵
        Omega(np.array): 观点置信度矩阵
        tau(float): 为均衡收益方差的刻度值，体现了对个人观点在总体估计中的权重

    Returns:
        dict: 最小方差组合的权重信息，键为资产名，值为权重
    """
    
    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        weights = np.array([1.])
        weights_dict = {assets[0]: 1.}
    else:
        output = describe(return_table, is_print=False)
        covmat =(output['covariance_matrix'])
        expected_return = output['annualized_return'].iloc[0, :]
    
        # 求解调整后的期望收益、方差
        adjustedReturn = expected_return + tau*covmat.dot(P.transpose()).dot(np.linalg.inv(Omega+tau*(P.dot(covmat).dot(P.transpose())))).dot(Q - P.dot(expected_return))
        right = (tau)*covmat.dot(P.transpose()).dot(np.linalg.inv(Omega+P.dot(covmat).dot(P.transpose()))).dot(P.dot(tau*covmat))
        right = right.transpose()
        right = right.set_index(expected_return.index)
        M = tau*covmat - right
        Sigma_p = covmat + M
        adjustedReturn = adjustedReturn.as_matrix()
        Sigma_p = matrix(Sigma_p.as_matrix())

        P = 2 * Sigma_p
        q = matrix(np.zeros(n_asset))

        if allow_short:
            G = matrix(0., (n_asset, n_asset))
        else:
            G = matrix(np.diag(-1 * np.ones(n_asset)))
        
        h = matrix(0., (n_asset, 1))
        A = matrix(np.ones(n_asset)).T
        b = matrix([1.0])
        solvers.options['show_progress'] = False
        sol = solvers.qp(P, q, G, h, A, b)
        weights = np.array(sol['x'].T)[0]
        weights_dict = dict(zip(assets, weights))

    r = np.dot(weights, output['annualized_return'].iloc[0, :].as_matrix())
    v = np.sqrt(np.dot(np.dot(weights, Sigma_p), weights.T))

    if show_details:
        print("""
Minimum Variance Portfolio:
    Short Allowed: {}
    Portfolio Return: {}
    Portfolio Volatility: {}
    Portfolio Weights: {}
""".format(allow_short, r, v, "\n\t{}".format("\n\t".join("{}: {:.1%}".format(k, v) for k, v in weights_dict.items()))).strip())
    
    return weights_dict
#计算最大效用组合，目标函数为：期望年化收益率 - 风险厌恶系数 * 期望年化方差，风险厌恶系数，越大表示对风险越厌恶，默认为3.0

def get_BL_maximum_utility_portfolio(return_table,tau=0.05,P=None,Q=None,Omega=None, risk_aversion=3., allow_short=False, show_details=True):
    """
    计算最大效用组合，目标函数为：期望年化收益率 - 风险厌恶系数 * 期望年化方差
    
    Args:0
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        risk_aversion (float): 风险厌恶系数，越大表示对风险越厌恶，默认为3.0
        allow_short (bool): 是否允许卖空
        show_details (bool): 是否显示细节
        P(np.array): 观点矩阵
        Q(np.array): 观点收益矩阵
        Omega(np.array): 观点置信度矩阵
        tau(float): 为均衡收益方差的刻度值，体现了对个人观点在总体估计中的权重

    Returns:
        dict: 最小方差组合的权重信息，键为资产名，值为权重
    """
    
    import numpy as np
    from cvxopt import matrix, solvers

    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        weights = np.array([1.])
        weights_dict = {assets[0]: 1.}
    else:
        output = describe(return_table, is_print=False)
        covmat =(output['covariance_matrix'])
        expected_return = output['annualized_return'].iloc[0, :]
    
        # 求解调整后的期望收益、方差
        adjustedReturn = expected_return + tau*covmat.dot(P.transpose()).dot(np.linalg.inv(Omega+tau*(P.dot(covmat).dot(P.transpose())))).dot(Q - P.dot(expected_return))
        right = (tau)*covmat.dot(P.transpose()).dot(np.linalg.inv(Omega+P.dot(covmat).dot(P.transpose()))).dot(P.dot(tau*covmat))
        right = right.transpose()
        right = right.set_index(expected_return.index)
        M = tau*covmat - right
        Sigma_p = covmat + M
        adjustedReturn = adjustedReturn.as_matrix()
        Sigma_p = matrix(Sigma_p.as_matrix())

        if abs(risk_aversion) < 0.01:
            max_ret = max(adjustedReturn)
            weights = np.array([1. if adjustedReturn[i] == max_ret else 0. for i in range(n_asset)])
            weights_dict = {asset: weights[i] for i, asset in enumerate(assets)}
        else:
            P = risk_aversion * Sigma_p
            q = matrix(-adjustedReturn.T)

            if allow_short:
                G = matrix(0., (n_asset, n_asset))
            else:
                G = matrix(np.diag(-1 * np.ones(n_asset)))

            h = matrix(0., (n_asset, 1))
            A = matrix(np.ones(n_asset)).T
            b = matrix([1.0])
            solvers.options['show_progress'] = False
            sol = solvers.qp(P, q, G, h, A, b)
            weights = np.array(sol['x'].T)[0]
            weights_dict = dict(zip(assets, weights))

    r = np.dot(weights, output['annualized_return'].iloc[0, :].as_matrix())
    v = np.sqrt(np.dot(np.dot(weights, Sigma_p), weights.T))
    
    if show_details:
        print("""
Maximum Utility Portfolio:
    Risk Aversion: {}
    Short Allowed: {}
    Portfolio Return: {}
    Portfolio Volatility: {}
    Portfolio Weights: {}
""".format(risk_aversion, allow_short, r, v, "\n\t{}".format("\n\t".join("{}: {:.1%}".format(k, v) for k, v in weights_dict.items()))).strip())

    
    return weights_dict

def get_BL_efficient_frontier(return_table,tau=0.05,P=None,Q=None,Omega=None,allow_short=False, n_samples=25):
    """
    计算Efficient Frontier
    
    Args:
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        n_samples (int): 用于计算Efficient Frontier的采样点数量
        P(np.array): 观点矩阵
        Q(np.array): 观点收益矩阵
        Omega(np.array): 观点置信度矩阵
        tau(float): 为均衡收益方差的刻度值，体现了对个人观点在总体估计中的权重

    Returns:
        DataFrame: Efficient Frontier的结果，列为"returns", "risks", "weights"
    """
    
    import numpy as np
    import pandas as pd
    from cvxopt import matrix, solvers
    
    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        raise ValueError("There must be at least 2 assets to calculate the efficient frontier!")

    output = describe(return_table, is_print=False)
    covmat =(output['covariance_matrix'])
    expected_return = output['annualized_return'].iloc[0, :]
    
    # 求解调整后的期望收益、方差
    adjustedReturn = expected_return + tau*covmat.dot(P.transpose()).dot(np.linalg.inv(Omega+tau*(P.dot(covmat).dot(P.transpose())))).dot(Q - P.dot(expected_return))
    right = (tau)*covmat.dot(P.transpose()).dot(np.linalg.inv(Omega+P.dot(covmat).dot(P.transpose()))).dot(P.dot(tau*covmat))
    right = right.transpose()
    right = right.set_index(expected_return.index)
    M = tau*covmat - right
    Sigma_p = covmat + M
    adjustedReturn = adjustedReturn.as_matrix()
    Sigma_p = matrix(Sigma_p.as_matrix())
	
    risks, returns, weights = [], [], []
    for level_return in np.linspace(min(adjustedReturn), max(adjustedReturn), n_samples):
        P = 2 * Sigma_p
        q = matrix(np.zeros(n_asset))
        
        if allow_short:
            G = matrix(0., (n_asset, n_asset))
        else:
            G = matrix(np.diag(-1 * np.ones(n_asset)))
        
        h = matrix(0., (n_asset, 1))    
        A = matrix(np.row_stack((np.ones(n_asset), adjustedReturn)))
        b = matrix([1.0, level_return])
        solvers.options['show_progress'] = False
        sol = solvers.qp(P, q, G, h, A, b)
        risks.append(np.sqrt(sol['primal objective']))
        returns.append(level_return)
        weights.append(dict(zip(assets, list(sol['x'].T))))
    
    output = {"returns": returns,
              "risks": risks,
              "weights": weights}
    output = pd.DataFrame(output)
    return output

def get_maximum_sharpe_portfolio(return_table, riskfree_rate=0.,tau=0.05,P=None,Q=None,Omega=None,allow_short=False, show_details=True):
    """
    计算最大效用组合，目标函数为：（期望年化收益率 - 无风险收益率）/ 期望年化方差
    
    Args:
        return_table (DataFrame): 收益率矩阵，列为资产，值为按日期升序排列的收益率
        riskfree_rate (float): 无风险收益率
        allow_short (bool): 是否允许卖空
        show_details (bool): 是否显示细节
        P(np.array): 观点矩阵
        Q(np.array): 观点收益矩阵
        Omega(np.array): 观点置信度矩阵
        tau(float): 为均衡收益方差的刻度值，体现了对个人观点在总体估计中的权重

    Returns:
        dict: 最小方差组合的权重信息，键为资产名，值为权重
    """
    
    import numpy as np
    from cvxopt import matrix, solvers

    assets = return_table.columns
    n_asset = len(assets)
    if n_asset < 2:
        output = describe(return_table, is_print=False)
        r = output['annualized_return'].iat[0, 0]
        v = output['annualized_volatility'].iat[0, 0]
        weights_dict = {assets[0]: 1.}
    else:
        efs = get_BL_efficient_frontier(return_table,tau,P=P,Q=Q,Omega=Omega,allow_short=allow_short, n_samples=100)
        i_star = max(range(100), key=lambda x: (efs.at[x, "returns"] - riskfree_rate) / efs.at[x, "risks"])
        r = efs.at[i_star, "returns"]
        v = efs.at[i_star, "risks"]
        weights_dict = efs.at[i_star, "weights"]

    s = (r - riskfree_rate) / v
    
    if show_details:
        print("""
Maximum Sharpe Portfolio:
    Riskfree Rate: {}
    Short Allowed: {}
    Portfolio Return: {}
    Portfolio Volatility: {}
    Portfolio Sharpe: {}
    Portfolio Weights: {}
""".format(riskfree_rate, allow_short, r, v, s, "\n\t{}".format("\n\t".join("{}: {:.1%}".format(k, v) for k, v in weights_dict.items()))).strip())
    
    return weights_dict

def draw_efficient_frontier(effcient_frontier_output):
    """
    绘出Efficient Frontier
    
    Args:
        effcient_frontier_output: Efficient Frontier的计算结果，即get_efficient_frontier的输出
    """

    import seaborn
    from matplotlib import pyplot as plt

    fig = plt.figure(figsize=(7, 4))
    ax = fig.add_subplot(111)
    ax.plot(effcient_frontier_output['risks'], effcient_frontier_output['returns'])
    ax.set_title('Efficient Frontier', fontsize=14)
    ax.set_xlabel('Standard Deviation', fontsize=12)
    ax.set_ylabel('Expected Return', fontsize=12)
    ax.tick_params(labelsize=12)
    plt.show()

def create_equal_difference_balanced_dates(start,end,dt):
    cal = get_calendar()
    dates = cal.sessions_in_range(start, end)
    balance_dates = []
    for i in range(len(dates)):
        if i % dt== 0:
            balance_dates.append(dates[i].date())
    return balance_dates
def create_balanced_dates(start,end,instruments,method):
    if method == 'equal_difference':
        return create_equal_difference_balanced_dates(start,end,instruments['dt'])
    
    