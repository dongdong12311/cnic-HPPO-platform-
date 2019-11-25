# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:39:16 2019

@author: Administrator
"""
import datetime
import pandas as pd

    
class _Portfolio:
    def __init__(self,trade_date,cash,market_value,static_unit_net_value,
                 total_value,unit_net_value,units):
        self.trade_date = trade_date
        self.cash = cash
        self.market_value = market_value
        self.static_unit_net_value = static_unit_net_value
        self.total_value = total_value
        self.units = units
        self.unit_net_value = unit_net_value
class _Position:
    def __init__(self,trade_date,avg_price,last_price,market_value,order_book_id,quant,symbol):
        self.trade_date = trade_date
        self.avg_price = avg_price
        self.last_price = last_price
        self.market_value = market_value
        self.order_book_id= order_book_id
        self.quant = quant
        self.symbol = symbol
class _Account:
    def __init__(self,trade_date,cash,dividend_receivable,market_value,total_value,transaction_cost):
        self.trade_date = trade_date
        self.cash  = cash
        self.dividend_receivable = dividend_receivable
        self.market_value = market_value
        self.total_value = total_value
        self.transaction_cost = transaction_cost
class _Trade:
    def __init__(self,trade_date,commission,
                 exec_id,last_price,
                 last_quantity,
                 order_book_id,
                 order_id,
                 position_effect,
                 side,symbol,tax,
                 trading_datetime,
                 transaction_cost):
        self.trade_date = trade_date
        self.commission = commission
        self.exec_id = exec_id
        self.last_price = last_price
        self.last_quantity = last_quantity
        self.order_book_id = order_book_id
        self.order_id = order_id
        self.position_effect = position_effect
        self.side = side
        self.symbol = symbol
        self.tax = tax
        self.trading_datetime= trading_datetime
        self.transaction_cost = transaction_cost 
class _Benchmark:
    def __init__(self,trade_date,cash,market_value,static_unit_net_value,
                 total_value,unit_net_value,units):
        self.trade_date = trade_date
        self.cash = cash
        self.market_value = market_value
        self.static_unit_net_value = static_unit_net_value
        self.total_value = total_value
        self.unit_net_value = unit_net_value
        self.units = units
class Analyser:
    def __init__(self):
        self.res = {'sys_analyser':
            {
                 'portfolio':{},
                'stock_positions':{},
                'summary':{},
                'stock_account':{},
                'trade':{},
                'benchmark_portfolio':{}
            }
            }
        self._port = []
        self._benchmark_portfolio = []
        self._stock_account = []
        self._positions = []
        self._trades = []

    def _transform(self):
        "transfer position to frame______________"
        #self.res['sys_analyser']['positions'] = self._positions
        
        "__________________portfolio__________________"
        temp =  pd.DataFrame(self._port,columns =
                         ['trade_date','cash', 'market_value', 'static_unit_net_value', 'total_value',
       'unit_net_value', 'units'])
        temp.index = temp['trade_date']
        temp = temp.drop(['trade_date'],axis=1)
        self.res['sys_analyser']['portfolio'] = temp
        
        temp = pd.DataFrame(self._positions,columns = ['trade_date',
                                                       'avg_price',
                                                       'last_price',
                                                       'market_value',
                                                       'order_book_id',
                                                       'quant','symbol'])
        temp.index = temp['trade_date']
        temp = temp.drop(['trade_date'],axis=1)
        self.res['sys_analyser']['stock_positions'] = temp 
        
        
        "__________________trade_____________________"
        temp = pd.DataFrame(self._trades,columns = ['trade_date','commission',
                 'exec_id','last_price',
                 'last_quantity',
                 'order_book_id',
                 'order_id',
                 'position_effect',
                 'side','symbol','tax',
                 'trading_datetime',
                 'transaction_cost'])
        temp.index = temp['trade_date']
        temp = temp.drop(['trade_date'],axis=1)
        self.res['sys_analyser']['trade'] = temp         
        
        
        "_________________stock_account______________________"
        temp = pd.DataFrame(self._stock_account,columns = ['trade_date',
                                                           'cash',
                                                           'dividend_receivable',
                                                           'market_value',
                                                           'total_value',
                                                           'transaction_cost'])
        temp.index = temp['trade_date']
        temp = temp.drop(['trade_date'],axis=1)
        self.res['sys_analyser']['stock_account'] = temp          
        
        
        #_________________bench_mark______________________
        temp = pd.DataFrame(self._benchmark_portfolio,columns = [
                'trade_date',
                'cash','market_value',
                'static_unit_net_value',
                 'total_value',
                 'unit_net_value',
                 'units'])
        temp.index = temp['trade_date']
        temp = temp.drop(['trade_date'],axis=1)
        self.res['sys_analyser']['benchmark_portfolio'] = temp           
        
    def append_trades(self,trade_date,commission,
                 exec_id,last_price,
                 last_quantity,
                 order_book_id,
                 order_id,
                 position_effect,
                 side,symbol,tax,
                 trading_datetime,
                 transaction_cost):
        self._trades.append([trade_date,
                             commission,
                             exec_id,
                             last_price,
                             last_quantity,
                             order_book_id,
                             order_id,
                             position_effect,
                             side,
                             symbol,
                             tax,
                             trading_datetime,
                             transaction_cost])
    def append_position(self,trade_date,avg_price,last_price,
                        market_value,order_book_id,
                        quant,symbol):
        self._positions.append([trade_date,
                                avg_price,
                                last_price,
                                market_value,
                                order_book_id,
                                quant,
                                symbol])
    def append_stock_account(self,trade_date,
                                  cash,
                                  dividend_receivable,
                                  market_value,
                                  total_value,
                                  transaction_cost):
        self._stock_account.append([trade_date,
                                    cash,
                                    dividend_receivable,
                                    market_value,
                                    total_value,
                                    transaction_cost])
    def append_benchmark_portfolio(self,
                                   trade_date,
                                   cash,
                                   market_value,
                                   static_unit_net_value,
                                   total_value,
                                   unit_net_value,
                                   units):
        self._benchmark_portfolio.append([trade_date,
                                     cash,
                                     market_value,
                                     static_unit_net_value,
                                     total_value,
                                     unit_net_value,
                                     units])
    def append_portfolio(self,trade_date,cash,market_value,static_unit_net_value,
                 total_value,unit_net_value,units):
        self._port.append([trade_date,
                           cash,
                           market_value,
                           static_unit_net_value,
                           total_value,
                           unit_net_value,
                           units])
    
    
    def get_result(self):
        self._transform()
        return self.res