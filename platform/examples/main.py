# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:05:48 2019

@author: dongdong
"""

from trading_system.engine import Run_func
from trading_system.plot.plot import plot_result
from trading_system.generate_parameter import generate,print_tree,generate_all_param
import json
from bayes_opt import BayesianOptimization
import sys
sys.path.append('/home/dongdong/桌面/platform/examples')
with open('hpr.json') as f:
    config =  json.load(f)
try:
    my_stragety = __import__(config['stragety'])
except:
    print("could not read config.stragety")
result = []

def get_sharp(config):
    res = Run_func(my_stragety.initialize,my_stragety.handle_data,config)
    return res['sys_analyser']['summary']['sharpe']

def grid_search(config):
    result = []
    params,all_param = generate_all_param(config)
    for param in all_param:
        for i in range(len(param)):
            config[params[i]] = param[i]
        result.append({ 'param': param,'sharpe':get_sharp(config)})  
    return result

def _bayesian_search(**kargs):
    for key in kargs:
        config[key] = kargs[key]
        if config['opt_param'][key]['data_type'] == 'int':
            config[key] = int(config[key])
    return -get_sharp(config)

def bayesian_search(config):
    pbounds = generate_pbounds(config['opt_param'])
    optimizer = BayesianOptimization(
        f=_bayesian_search,
        pbounds=pbounds,
        verbose=2, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
        random_state=1,
    )
    optimizer.maximize(
        init_points=2,
        n_iter=10,
    )
def generate_pbounds(dic):
    res = {}
    for key in dic:
        start = dic[key]['start']
        end = dic[key]['start'] + dic[key]['step'] * (dic[key]['dt'] -1)
        res.update({key:(start,end)})
    return res
def get_data_type(dic):
    data_type = {}
    for key in dic:
        data_type.update({key: dic['data_type']})
        
if len(config['opt_param']):
    res = grid_search(config)


else:
    res = Run_func(my_stragety.initialize,my_stragety.handle_data,config)
    result.append(res)
    
