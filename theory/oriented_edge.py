import scipy as sp
import numpy as np
from scipy.sparse.csgraph import maximum_flow
from scipy.sparse import csr_matrix

from theory.tools import *

def build_flow_max_graph(n, mat):
    
    sum_line, sum_col = compute_degrees(mat)
    surcharge,souscharge = compute_charge(sum_line, sum_col, n)
                
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
    m = mat.copy()
    graph = flow_graph(n, m).toarray()
    
    for i in range(n):
        for j in range(n):
            w = graph[i][j]
            if (w > 0):
                m[i][j] = 0
            elif (w == 0):
                if (m[i][j] > 0):
                    m[j][i] = 0
                    
    return m