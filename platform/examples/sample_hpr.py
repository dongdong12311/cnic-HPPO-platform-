# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 01:57:22 2019

@author: dongdong
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:06:30 2019

@author: dongdong
"""

'this example is given to realize the cvar model '
from pypfopt import hierarchical_risk_parity
import pandas as pd
from trading_system.api.api import create_balanced_dates
    

 

def initialize(context):

    print('initialized!')

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
        model = hierarchical_risk_parity.HRPOpt(history_prices.pct_change().dropna())
        weights = model.hrp_portfolio()
        weight = []
        prices = []
        for code in context.stocks:
            weight.append(weights[code])
            prices.append(data.latest_price(code,"1d"))
        data.order_target_percent(context.stocks, weight,prices)    

