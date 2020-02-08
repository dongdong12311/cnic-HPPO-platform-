# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:31:43 2019

@author: Administrator
"""
import os,sys
sys.path.append("..") 
from dataset.const import stock_index_path,base_path

from dataset.update_data import update_stock_index
file_path = os.path.join(base_path,stock_index_path)
a = update_stock_index(file_path)