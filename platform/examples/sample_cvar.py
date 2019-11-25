# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 11:14:27 2019

@author: dongdong
"""

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
from pypfopt import value_at_risk
import pandas as pd




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
        model = value_at_risk.CVAROpt(history_prices.pct_change().dropna())
        try:           
            weights = model.min_cvar(beta = context.beta)
        except:
            return 
        weight = []
        prices = []
        for code in context.stocks:
            weight.append(weights[code])
            prices.append(data.latest_price(code,"1d"))
        data.order_target_percent(context.stocks, weight,prices)    

