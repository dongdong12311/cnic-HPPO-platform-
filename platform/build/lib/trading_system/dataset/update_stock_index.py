# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:31:43 2019

@author: Administrator
"""
import os
from const import stock_index_path,base_path

from update_data import update_stock_index
file_path = os.path.join(base_path,stock_index_path)
a = update_stock_index(file_path)