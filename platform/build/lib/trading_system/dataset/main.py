#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:14:13 2019
main function is used to save daily data to csv file 
@author: dongdong
"""
from const import *

from create_data import CreateMeta
from  update_data import Update
from ts_api import GetStockList
import os
stockcodes = GetStockList()

#code_list = CodeList()



for code in stockcodes:       
    file = os.path.join(base_data_path,code)
    'if there is a new stock code create it'
    CreateMeta(file,metas)
    Update(file,code)
