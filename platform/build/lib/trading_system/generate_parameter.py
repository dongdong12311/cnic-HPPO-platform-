#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 14:49:46 2019

@author: dongdong
"""

class Node:
    def __init__(self,value):
        self.children = []
        self.value = value

        
import copy

def print_tree(node,path,res):
    path.append(node.value)
    if not len(node.children):
        temp  = copy.copy(path)
        res.append(temp)
        return 
        
    for node in node.children:
        temp  = copy.copy(path)
        print_tree(node,temp,res)
            
            
def create_node():
    return Node(0)

def create_nodes(data,node):
    for i in range(data):
        node.children.append(Node(i))
        
    return node.children
def generate(datas):
    head = create_node()
    nodes = [head]
    for i in range(len(datas)):
        data = datas[i]
        temp = []
        for node in nodes:   
            temp += create_nodes(data,node)
        
        nodes = temp
    return head
def generate_all_param(config): 
    all_param = []
    if len(config['opt_param']):
        params = list(config['opt_param'].keys())
        temp = []
        for param in params:
            temp.append(config['opt_param'][param]['dt'])
    
        head = generate(temp)
        res = [] 
        print_tree(head,[],res)
        for i  in range(len(res)):
            res[i] = res[i][1:]
        
        for d in res:
            p = []
            for i in range(len(d)):            
                p.append(config['opt_param'][params[i]]['start'] + config['opt_param'][params[i]]['step'] * d[i])
            all_param.append(p)
    return params,all_param