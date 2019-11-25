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

def required_argument():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--start', type=int,required = True, help = "start date")
    arg_parser.add_argument('--end', type=int,required = True, help = "end date")
    arg_parser.add_argument('--initial_capital', type=float,required = True, help = " initial capital")
    arg_parser.add_argument('--stragety', type=str,required = True, help = "stragety name ")
    arg_parser.add_argument('--benchmark', type=str,required = True, help = "benchmark name ")
    args=arg_parser.parse_args()
    return args

arg = required_argument()
_stragety = arg.stragety 
stragety = __import__(_stragety)



config = {
            'start':arg.start,
            'end':arg.end,
            'initial_capital':arg.initial_capital,
            'benchmark':arg.benchmark
          }

res = Run_func(stragety.initialize,stragety.handle_data,config)
plot_result(res['sys_analyser'])