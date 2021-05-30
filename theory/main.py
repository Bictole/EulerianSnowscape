# -*- coding: utf-8 -*-
"""
Created on Sat May 29 18:33:09 2021

@author: morin
"""
from eulerian import build_adj_mat_weighted
from eulerian import make_eulerian
from oriented_edge import orient_graph

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

def mat_to_edges(n, mat):
    edge =  []
    for i in range(n):
        for j in range(n):
            if (mat[i][j]):
                edge.append((i,j,mat[i][j]))
    return edge

def main(n, edges):
    #print_graph_with_weights(n,edges)
    mat = build_adj_mat_weighted(n,edges)
    oriented_mat = orient_graph(n, mat)
    final_mat = make_eulerian(n, mat, oriented_mat, edges)
    print_graph_with_weights(n,mat_to_edges(n,final_mat))
    

main(4, [(0,1,3),(0,2,11),(1,2,5),(2,3,1),(3,0,3), (0,3,3), (2,1,5), (1,0,3)])
    
#print_graph_with_weights(3,[(0,1,1),(1,2,1),(2,0,1),(0,2,1)])
#print(flow_graph(3,[(0,1),(1,2),(2,0),(0,2)]))
    