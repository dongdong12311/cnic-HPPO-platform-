# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 18:20:02 2019

@author: Administrator
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新日线交易日历的数据
Created on Wed Jul 17 22:14:13 2019
main function is used to save daily data to csv file 
@author: dongdong
"""
from const import trading_calendar_path,trading_calendar_meta,base_path

from create_data import CreateMeta
from  update_data import Update_daily_trading_calendar
from ts_api import GetStockList
import os
stockcodes = GetStockList()

#code_list = CodeList()


"create  daily_trading_calendar"
file = os.path.join(os.path.join(base_path,trading_calendar_path),trading_calendar_path)
CreateMeta(file,trading_calendar_meta)
Update_daily_trading_calendar(file)
