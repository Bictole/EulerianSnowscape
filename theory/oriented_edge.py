# -*- coding: utf-8 -*-
"""
Created on Sat May 29 16:29:27 2021

@author: morin
"""
from eulerian import build_adj_mat
import scipy as sp
import numpy as np
from scipy.sparse.csgraph import maximum_flow
from scipy.sparse import csr_matrix



def build_flow_max_graph(n, mat):
    sum_col = np.sum(mat, axis=0)
    sum_line = np.sum(mat, axis=1)
    souscharge = []
    surcharge = []
    
    for i in range(n):
        if (sum_col[i] > sum_line[i]):
            souscharge.append(i)
                
        elif (sum_line[i] > sum_col[i]):
            surcharge.append(i)
                
    result = build_capacity_mat(n+2, mat)
    
    source = n
    sink = n + 1
    for i in surcharge:
        result[source][i] = sum_line[i] - sum_col[i]
    for j in souscharge:
        result[j][sink] = sum_col[j] - sum_line[j]
        
        
    return result


def build_capacity_mat(n, mat):
    M = []
    for i in range (0, n):
        M.append([0]*n)
        
    for i in range(n-2):
        for j in range(n-2):
            if (mat[i][j] and mat[j][i]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def flow_graph(n, mat):
    capacity_mat = build_flow_max_graph(n,mat)
    graph = csr_matrix(capacity_mat)
    flow = maximum_flow(graph, n, n+1)
    return flow.residual

def orient_graph(n, mat):
    graph = flow_graph(n, mat).toarray()
    for i in range(n):
        for j in range(n):
            w = graph[i][j]
            if (w > 0):
                mat[i][j] = 0
            elif (w == 0):
                if (mat[i][j] == 1):
                    mat[j][i] = 0
            
    return mat
    
    
    