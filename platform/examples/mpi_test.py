# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 02:05:48 2019

@author: dongdong
"""

from trading_system.engine import Run_func
import json
from trading_system.generate_parameter import generate,print_tree,generate_all_param

import sys
with open('markowitz.json') as f:
    config =  json.load(f)
my_stragety = __import__(config['stragety'])

result = []

def get_sharp(config):
    res = Run_func(my_stragety.initialize,my_stragety.handle_data,config)
    return res['sys_analyser']['summary']['sharpe']
import mpi4py.MPI as MPI
 
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

def cal_config_param_i(config,params,all_param,comm_rank):
    result = []
    
    n = len(all_param)
    while comm_rank < n: 
        param = all_param[comm_rank]       
        for i in range(len(param)):
            config[params[i]] = param[i] 
        sharp = get_sharp(config)
        result.append({ 'param': param,'sharpe':sharp }) 
        comm_rank += comm_size
    return result

def grid_search(config):
    result = []
    params,all_param = generate_all_param(config)
    if comm_rank == 0:
        result = cal_config_param_i(config,params,all_param,0)
        for i in range(1,comm_size):        
            data_recv =comm.recv(source=i)
            result += data_recv
        return result
    else:
        data_send = cal_config_param_i(config,params,all_param,comm_rank)
        comm.send(data_send,dest = 0)
    return 
        
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
import time
tic = time.time()        
if len(config['opt_param']):
    res = grid_search(config)
    if comm_rank == 0:
        print(res)
        toc = time.time()
        print(toc - tic)