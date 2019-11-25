# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:20:29 2018

@author: Administrator
"""

import os 
class Log:
    def __init__(self,filename,filepath):
        name = os.path.join(filepath,filename)
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        self.__file = open(name,'w')
    def write(self,s):
        self.__file.write(s)
        self.__file.write('\n')
    def __del__(self):       
        self.__file.close()
        

    

    
        
		
