# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 19:29:41 2019

@author: Administrator
"""

from dataset.dataframe_to_bundle import DataFrameToBundle
from dataset.const import  base_path,bcolz_data_path,metas
from dataset.const import  trading_calendar_path,trading_calendar_meta
from dataset.const import  stock_index_path,stock_index_metas
import os
from dataset.const import daily_data_path
import numpy as np
a = DataFrameToBundle()

"日线数据"

dtypes = [np.uint32]*len(metas)
file_path = os.path.join(base_path,daily_data_path)
target_path = os.path.join(os.path.join(base_path,bcolz_data_path),daily_data_path)
a.to_bundle(file_path,target_path,metas,dtypes)

"交易日历数据"
dtypes = [np.uint32]
filepath = os.path.join(base_path,trading_calendar_path)
target = os.path.join(os.path.join(base_path,bcolz_data_path),trading_calendar_path)
a.to_bundle(filepath,target,trading_calendar_meta,dtypes)

"指数数据"
dtypes = [np.uint32]*10
filepath = os.path.join(base_path,stock_index_path)
target = os.path.join(os.path.join(base_path,bcolz_data_path),stock_index_path)
a.to_bundle(filepath,target,stock_index_metas,dtypes)


