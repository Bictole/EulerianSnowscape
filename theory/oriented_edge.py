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

import networkx as nx
from networkx.algorithms.shortest_paths import weighted

def print_graph_with_weights(n, edges):
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from(edges)
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G,'weight')
    weight_labels = {}
    for a in labels:
        weight_labels[(a[0], a[1])] = labels[a]
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)
    return G , pos

def build_flow_max_graph(n ,edges):
    mat = build_adj_mat(n,edges)
    sum_col = np.sum(mat, axis=0)
    sum_line = np.sum(mat, axis=1)
    souscharge = []
    surcharge = []
    
    for i in range(n):
        if (sum_col[i] > sum_line[i]):
            souscharge.append(i)
                
        elif (sum_line[i] > sum_col[i]):
            surcharge.append(i)
                
    result = build_capacity_mat(n+2, mat, edges)
    
    source = n
    sink = n + 1
    for i in surcharge:
        result[source][i] = sum_line[i] - sum_col[i]
    for j in souscharge:
        result[j][sink] = sum_col[j] - sum_line[j]
        
        
    return result


def build_capacity_mat(n, mat, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        if (mat[edge[0]][edge[1]] and mat[edge[1]][edge[0]]):
            M[edge[0]][edge[1]] = 1
            M[edge[1]][edge[0]] = 1
    return M

def flow_graph(n, edges):
    capacity_mat = build_flow_max_graph(n,edges)
    graph = csr_matrix(capacity_mat)
    print(graph, "\n")
    flow = maximum_flow(graph, n, n+1)
    return flow.residual


print_graph_with_weights(4, [(0,1,3),(0,2,11),(1,2,5),(2,3,1),(3,0,3), (0,3,3), (2,1,5), (1,0,3)])
print(flow_graph(4, [(0,1,3),(0,2,11),(1,2,5),(2,3,1),(3,0,3), (0,3,3), (2,1,5), (1,0,3)]))
    
#print_graph_with_weights(3,[(0,1,1),(1,2,1),(2,0,1),(0,2,1)])
#print(flow_graph(3,[(0,1),(1,2),(2,0),(0,2)]))
    
    