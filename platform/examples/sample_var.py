#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 09:45:24 2019

@author: dongdong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:06:30 2019

@author: dongdong
"""

'this example is given to realize the cvar model '
from pypfopt import value_at_risk,hierarchical_risk_parity
from trading_system.dataset.base_data_source import BaseDataSource
from trading_system.dataset.const  import base_path,bcolz_data_path
import os
import pandas as pd
import datetime
from trading_system.api.api import get_calendar
cal = get_calendar()
start = 20150101
end = 20151212
dates = cal.sessions_in_range(start, end)

balance_dates = []
for i in range(len(dates)):
    if i%20== 0:
        balance_dates.append(dates[i].date())
        
STOCKS = ['000001.SZ','000002.SZ','000004.SZ','000005.SZ','000006.SZ','000007.SZ',
          '000008.SZ','000009.SZ','000010.SZ']

risk_free_rate = 0.02   
cleaned_weights = True
expected_return_days = 100 #利用多久的数据估算
def initialize(context):
    context.stocks = STOCKS

    context.expected_return_days = expected_return_days

    context.tick  = 0
    context.balance_dates = balance_dates
    context.cleaned_weights = cleaned_weights
    context.risk_free_rate = risk_free_rate

    print('initialized!')
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
        model = value_at_risk.CVAROpt(history_prices.pct_change().dropna())
        weights = model.min_cvar()
        weight = []
        prices = []
        for code in context.stocks:
            weight.append(weights[code])
            prices.append(data.latest_price(code,"1d"))
        data.order_target_percent(context.stocks, weight,prices)    

