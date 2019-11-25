#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 21:06:55 2019

@author: dongdong
"""
from trading_system.engine import Run_func
from trading_system.plot.plot import plot_result
from trading_system.generate_parameter import generate,print_tree,generate_all_param
import json
with open('markowitz.json') as f:
    config =  json.load(f)
try:
    stragety = __import__(config['stragety'])
except:
    print("could not read config.stragety")    

res = Run_func(stragety.initialize,stragety.handle_data,config)

plot_result(res['sys_analyser'])