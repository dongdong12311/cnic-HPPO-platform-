# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 14:39:54 2020

@author: Administrator
"""

import mpi4py.MPI as MPI
 
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

def cal_xiaoyu_dengyu_100(i,rank):
    res= 0
    while 1:
        res +=i
        i += rank
        if i > 100:
            break
        
    return res

if comm_rank == 0:
    data_recv = [0]*comm_size
    res = cal_xiaoyu_dengyu_100(0,comm_size)
    for i in range(1,comm_size):        
        data_recv =comm.recv(source=i)
        res += data_recv
    print(res)
else:
    data_send = cal_xiaoyu_dengyu_100(comm_rank,comm_size)
    comm.send(data_send,dest = 0)
    

    
    