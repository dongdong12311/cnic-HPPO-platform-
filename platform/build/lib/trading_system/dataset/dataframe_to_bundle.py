#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 21:50:49 2019

@author: dongdong
"""

'create bundle once the bundle is created the meta can not be changed'

import bcolz
#from const import bcolz_data_path,metas,base_data_path
from .data_transform import change
import os
import numpy as np
from .localfile_to_dataframe import LocalFileToDataFrame
    
    
class DataFrameToBundle:
    def __init__(self):
        pass
    def to_bundle(self,base_data_path,bcolz_data_path,metas,dtypes):            
        base_data = []
        for i in range(len(metas)):
            base_data.append(np.array((),dtype = dtypes[i]))
        
        "create a table "
        data = bcolz.ctable(base_data, rootdir=bcolz_data_path, 
                         mode='w',names = metas)
        
        files = os.listdir(base_data_path)
        line_map  = {}
        begin_line = 0
        for file in files:
            print("load" + file)
            a =  LocalFileToDataFrame(os.path.join(base_data_path,file),file)
            if a is not None:
                for meta in metas:
                    a[meta] = change(a,meta)
                    
                for index in a.index:
                    data.append(list(a.loc[index]))
                end_line = begin_line + a.index.size - 1
                line_map.update({file:[begin_line,end_line]})
                begin_line = end_line + 1
        
        data.attrs['line_map'] = line_map
    
    
