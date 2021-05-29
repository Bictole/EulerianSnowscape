# -*- coding: utf-8 -*-
"""
Created on Sat May 29 16:29:27 2021

@author: morin
"""
from eulerian import *
import scipy as sp
import numpy as np

def build_flow_max_graph(n ,edges):
    mat = build_adj_mat(n,edges)
    sum_col = np.sum(mat, axis=0)
    sum_line = np.sum(mat, axis=1)
    souscharge = []
    surcharge = []
    
    for i in range(n):
        if (sum_col[i] > sum_line[i]):
            for k in range(sum_line[i], sum_col[i]):
                surcharge.append(i)
                
        elif (sum_line[i] > sum_col[i]):
            for k in range(sum_col[i], sum_line[i]):
                souscharge.append(i)
                
    source = n
    sink = n + 1
    
    for i in surcharge:
        edges.append((source,i,1))
    for j in souscharge:
        edges.append((j, sink, 1))
        
    return edges
