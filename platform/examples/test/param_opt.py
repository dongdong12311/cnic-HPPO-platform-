# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:05:48 2019

@author: dongdong
"""
import argparse
import os

from trading_system.engine import Run_func
from trading_system.dataset.const import base_path,bcolz_data_path
from trading_system.plot.plot import plot_result
from trading_system.generate_parameter import generate,print_tree
head = generate([5])
res = [] 
print_tree(head,[],res)
print(res)