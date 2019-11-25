#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 15:00:36 2019

@author: dongdong
"""
from .const import  TRADE_DATE,OPEN,HIGH,LOW,CLOSE
import numpy as np
def mul(data):
    return data * 10000
def donot_change(data):
    return data
change_rule = {TRADE_DATE:donot_change,OPEN:mul,
               HIGH:mul,LOW:mul,CLOSE:mul,'pre_close':mul
               ,'change':mul,'pct_chg':mul,'vol':donot_change,
               'amount':mul,'trade_date':donot_change}

def change(data,meta):
        return np.uint32(change_rule[meta](data[meta]))