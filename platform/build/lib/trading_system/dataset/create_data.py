#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:02:14 2019

@author: dongdong

1.from tushare to local data
2.read local data to pandas
3.pandas to bundle

"""

# get all stock code

import os
import csv

 
def CreateMeta(file_path,metas):
    if os.path.exists(file_path):
       return    
    with open(file_path,'w') as t_file:
        csv_writer = csv.writer(t_file)
        csv_writer.writerow(metas)
    return True

    
            

    
    
    