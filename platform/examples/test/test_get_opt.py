# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 15:33:33 2019

@author: dongdong
"""

#!/usr/bin/python
# -*- coding: gbk -*-
import sys
import getopt
import argparse
config_dic = {
        "start":int,
        "end":int,
        "initial_capital":float
        }

def required_argument():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--start', type=int,required = True, help = "start date")
    arg_parser.add_argument('--end', type=int,required = True, help = "end date")
    arg_parser.add_argument('--initial_capital', type=float,required = True, help = " initial capital")
    arg_parser.add_argument('--stragety', type=str,required = True, help = "stragety name ")
    arg_parser.add_argument('--benchmark', type=str,required = True, help = "benchmark name ")
    args=arg_parser.parse_args()
    return args
if __name__=="__main__":
    required_argument()