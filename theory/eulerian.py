# -*- coding: utf-8 -*-
"""
Created on Thu May  6 16:52:49 2021

@author: morin
"""

from scipy.optimize import linear_sum_assignment
import numpy as np
import math
import time
import sys

def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b,w) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def is_edge_connected(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b,w) in edges:
        succ[a].append(b)
        succ[b].append(a)
    # BFS over the graph, starting from one extremity of the first edge
    touched = [False] * n
    init = edges[0][0]
    touched[init] = True
    todo = [init]
    while todo:
        s = todo.pop()
        for d in succ[s]:
            if touched[d]:
                continue
            touched[d] = True
            todo.append(d)
    for a in range(n):
        if succ[a] and not touched[a]:
            return False
    return True

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

def build_adj_mat(n, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        M[edge[0]][edge[1]] = 1
    return M

def build_adj_mat_weighted(n, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        M[edge[0]][edge[1]] = edge[2]
    return M

def find_eulerian_cycle(n, edges):
    if len(edges) == 0:
        return []
    cycle = [edges[0][0]] # start somewhere
    while True:
        rest = []
        for (a, b) in edges:
            if cycle[-1] == a:
                cycle.append(b)
            elif cycle[-1] == b:
                cycle.append(a)
            else:
                rest.append((a,b))
        if not rest:
            assert cycle[0] == cycle[-1]
            return cycle[0:-1]
        edges = rest
        if cycle[0] == cycle[-1]:
            # Rotate the cycle so that the last state
            # has some outgoing edge in EDGES.
            for (a, b) in edges:
                if a in cycle:
                    idx = cycle.index(a)
                    cycle = cycle[idx:-1] + cycle[0:idx+1]
                    break
                
def single_source_distances(n,edges,src):
    # Classic Bellman-Ford for directed graphs
    dist = [math.inf] * n
    dist[src] = 0
    for k in range(n - 1):
        for (s, d, w) in edges:
            dist[d] = min(dist[d], dist[s] + w)
    # Extra loop to detect negative cycles
    for (s, d, w) in edges:
        if dist[d] > dist[s] + w:
            return None
    return dist

def all_pairs_shortest_path(n, cost):
    for k in range(n):
        print(k)
        for i in range(n):
            for j in range(n):
                if cost[i][k] + cost[k][j] < cost[i][j]:
                    cost[i][j] = cost[i][k] + cost[k][j]
    return cost

def add_edges(n, edges):
    '''
    mat = np.full((n,n), math.inf)
    for a , b, w in edges:
        mat[a][b] = w
    plus_court_chemin = all_pairs_shortest_path(n, mat)
    sys.stdout.write("Begin")
    for i in range(n):
        percent = i / n * 100
        start_time = time.time()
        plus_court_chemin.append(single_source_distances(n,edges, i))
        compute_time = time.time() - start_time
        time_left = compute_time * n - compute_time * i
        if (time_left / 60 > 1):
            nb_minutes = time_left // 60
            nb_seconds = time_left % 60
            sys.stdout.write("Processing: {:.2f}% - {} minutes and {:.2f} seconds left\n".format( percent, nb_minutes, nb_seconds))
        else:
            sys.stdout.write("Processing: {:.2f}% - {:.2f} seconds left\n".format( percent, time_left))
        sys.stdout.flush()
    '''
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
    
    bipartie = []
    indices_line = []
    indices_col = []
    dist = []
    compute_time = time.time()
    start_time = time.time()
    print(len(surcharge))
    print(len(souscharge))
    for j in range(n):
        if j in surcharge:
            percent = (j / len(surcharge)) * 100
            dist.append(single_source_distances(n, edges, j))
            compute_time = time.time() - start_time
            time_left = compute_time * (len(surcharge) - (j + 1)) / (j + 1)
            if (time_left / 60 > 1):
                nb_minutes = time_left // 60
                nb_seconds = time_left % 60
                sys.stdout.write("Processing: {:.2f}% - {} minutes and {:.2f} seconds left\n".format( percent, nb_minutes, nb_seconds))
            else:
                sys.stdout.write("Processing: {:.2f}% - {:.2f} seconds left\n".format( percent, time_left))
            sys.stdout.flush()
        else:
            dist.append([])
        
    for line,i in enumerate(souscharge):
        indices_line.append(i)
        weight = []
        for col,j in enumerate(surcharge):
            weight.append(dist[j][i])
            if (line == 0):
                indices_col.append(j)
        bipartie.append(weight)
        

    best_path = linear_sum_assignment(bipartie)

    for k in range(len(best_path[0])):
        i = best_path[0][k]
        j = best_path[1][k]
        edges.append((indices_col[j], indices_line[i], bipartie[i][j]))
                

    return edges
  

def make_eulerian_great_again(n, edges):
    add_edge = add_edges(n,edges)
    return is_eulerian(n, add_edge)


   

#print(add_edges(3, [(0,1,4),(1,2,3)]))
#print(add_edges(4, [(0,1,1),(0,2,1),(0,3,1)]))
#print(make_eulerian_great_again(9,[(0,1,3),(1,2,5),(1,5,4),(2,4,2),(2,3,4),(5,4,5),(5,6,3),(4,8,4),(4,6,6),(6,7,3),(8,6,4), (2,1,5),(4,2,2),(5,1,4),(6,4,6),(7,6,3),(5,0,7),(3,2,4)]))

    #print(add_edges(4,[(0,1,3),(0,2,11),(1,2,5),(2,3,1),(3,0,3)]))    
#print(add_edges(7, [(0, 1, 11), (0, 4, 3), (0, 5, 7), (0, 6, 5), (1, 2, 11), (2, 3, 11), (3, 0, 11), (4, 3, 1), (5, 2, 5), (6, 1, 3)]))    
    
    
    
    
    
    
    