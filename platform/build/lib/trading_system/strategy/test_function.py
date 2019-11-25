#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 21:45:34 2019

@author: dongdong
"""

def init(context):
    context.name = "dongdong"
    context.n = "24"
    
class test:
    name = ""
    def __init__(self):
        pass
     
t = test()
init(t)