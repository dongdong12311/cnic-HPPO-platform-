#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 12:18:52 2019

@author: dongdong
"""
config = {'markowitz':{  
    	    "stragety":"sample_markowitz",
            "start":20180101,
            "end":20181230,
            "initial_capital":1000000,
            "benchmark":"000001.SH",
            "balanced_dates":{"method":"equal_difference","param":20},
             "stocks" : ["000001.SZ","000002.SZ","000004.SZ","000005.SZ","000006.SZ","000007.SZ",
              "000008.SZ","000009.SZ","000010.SZ"],
             "expected_return_days" : 30,
             "cov_method" : "sample",
             "opt_criterion" : "max_sharpe",
             "cleaned_weights" : True,
             "target_return" : None,
             "target_risk"   : 0.1,
             "risk_free_rate" : 0.02,
             "opt_param":{"target_return":{"start":0.1,"step":0.01,"dt":3,"data_type":'float'},
                          "expected_return_days":{"start":10,"step":10,"dt":3,"data_type":'int'}}
             },
            'hpr':{  
    	    "stragety":"sample_hpr",
            "start":20180101,
            "end":20181230,
            "initial_capital":1000000,
            "benchmark":"000001.SH",
            "balanced_dates":{"method":"equal_difference","param":20},
             "stocks" : ["000001.SZ","000002.SZ","000004.SZ","000005.SZ","000006.SZ","000007.SZ",
              "000008.SZ","000009.SZ","000010.SZ"],
             "expected_return_days" : None,
             "cleaned_weights" : True,
             "opt_param":{"expected_return_days" : {"start":20,"step":10,"dt":3}}
             },
            'cvar':{  
    	    "stragety":"sample_cvar",
            "start":20180101,
            "end":20181230,
            "initial_capital":1000000,
            "benchmark":"000001.SH",
            "balanced_dates":{"method":"equal_difference","param":20},
             "stocks" : ["000001.SZ","000002.SZ","000004.SZ","000005.SZ","000006.SZ","000007.SZ",
              "000008.SZ","000009.SZ","000010.SZ"],
             "expected_return_days" : 30,
             "cleaned_weights" : True,
             "beta" :  None,
             "opt_param":{"beta" :  {"start":0.8,"step":0.01,"dt":10}}
             },
            'bl_model':{  
    	    "stragety":"sample_bl_model",
            "start":20180101,
            "end":20181230,
            "initial_capital":1000000,
            "benchmark":"000001.SH",
            "balanced_dates":{"method":"equal_difference","param":20},
             "stocks" : ["000001.SZ","000002.SZ","000004.SZ","000005.SZ","000006.SZ","000007.SZ"],
             "expected_return_days" : 30,
             "cleaned_weights" : True,
             "opt_param":[]
             },
        }
import json
for key in config.keys():
    file_name = key+'.json'
    print(file_name)
    with open(file_name,'w') as f:
        json.dump(config[key],f)
    

