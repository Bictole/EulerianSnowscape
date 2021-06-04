from operator import add
from networkx.algorithms.shortest_paths.unweighted import predecessor
from scipy.optimize import linear_sum_assignment
from scipy.sparse.csgraph import shortest_path
from scipy.sparse.csr import csr_matrix
from theory.graph import is_edge_connected_unoriented_weighted, predecessor_shortest_path, adjlist, check_balance_degree, is_edge_connected, np_build_adj_mat_directed_weighted, odd_vertices, is_edge_connected_weighted, odd_vertices_weighted, single_source_distances
import numpy as np
import math
import time
import sys

from theory.tools import *

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

def is_eulerian_weighted(n, edges):
    return is_edge_connected_weighted(n, edges) and not check_balance_degree(n, edges)

def is_eulerian_unoriented_weighted(n, edges):
    return is_edge_connected_unoriented_weighted(n, edges) and not odd_vertices_weighted(n, edges)

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

def find_eulerian_cycle_weighted(n, edges):
    if len(edges) == 0:
        return []
    cycle = [edges[0][0]] # start somewhere
    while True:
        rest = []
        for (a, b, w) in edges:
            if cycle[-1] == a:
                cycle.append(b)
            elif cycle[-1] == b:
                cycle.append(a)
            else:
                rest.append((a,b,w))
        if not rest:
            assert cycle[0] == cycle[-1]
            return cycle
        edges = rest
        if cycle[0] == cycle[-1]:
            # Rotate the cycle so that the last state
            # has some outgoing edge in EDGES.
            for (a, b, w) in edges:
                if a in cycle:
                    idx = cycle.index(a)
                    cycle = cycle[idx:-1] + cycle[0:idx+1]
                    break

def find_eulerian_cycle_weighted_custom(n, edges, nb_add_edges, predecessor):
    if len(edges) == 0:
        return []
    cycle = [edges[0][0]] # start somewhere
    added_edges = edges[-nb_add_edges:]
    while True:
        rest = []
        for (a, b, w) in edges:
            if cycle[-1] == a:
                if (a,b,w) in added_edges:
                    cycle += predecessor_shortest_path(a, b, predecessor)
                else:
                    cycle.append(b)
            else:
                rest.append((a,b,w))
        if not rest:
            assert cycle[0] == cycle[-1]
            return cycle
        edges = rest
        if cycle[0] == cycle[-1]:
            # Rotate the cycle so that the last state
            # has some outgoing edge in EDGES.
            for (a, b, w) in edges:
                if a in cycle:
                    idx = cycle.index(a)
                    cycle = cycle[idx:-1] + cycle[0:idx+1]
                    break

def make_eulerian(n, ort_mat, edges):
    sum_line,sum_col = compute_degrees(ort_mat)
    surcharge, souscharge = compute_charge(sum_line,sum_col,n)
    bipartie = []
    indices_line = []
    indices_col = []
    #dist = []
    start_time = time.time()
    count = 0
    mat = np_build_adj_mat_directed_weighted(n, edges)
    graph = csr_matrix(mat)
    dist, predecessor = shortest_path(graph, directed=True, unweighted=False, return_predecessors=True)
    '''
    for j in range(n):
        if j in souscharge:
            dist.append(single_source_distances(n, edges, j))
            # Display process status
            count += 1
            percent = (count / len(souscharge)) * 100
            compute_time = time.time() - start_time
            time_left = compute_time * (len(souscharge) - count) / count
            if (time_left / 60 > 1):
                nb_minutes = time_left // 60
                nb_seconds = time_left % 60
                sys.stdout.write("Processing: {:.2f}% - {} minutes and {:.2f} seconds left\n".format( percent, nb_minutes, nb_seconds))
            else:
                sys.stdout.write("Processing: {:.2f}% - {:.2f} seconds left\n".format( percent, time_left))
            sys.stdout.flush()
            # End 
        else:
            dist.append([])
    '''
    for line,i in enumerate(surcharge):
        weight = []
        for col,j in enumerate(souscharge):
            for k in range(sum_col[j] - sum_line[j]):
                weight.append(dist[col][i])
                if (line == 0):
                    indices_col.append(j)
        for k in range(sum_line[i] - sum_col[i]):
            indices_line.append(i)
            bipartie.append(weight)

    best_path = linear_sum_assignment(bipartie)

    euler_edges = mat_to_edges(n, ort_mat)
    for k in range(len(best_path[0])):
        i = best_path[0][k]
        j = best_path[1][k]
        euler_edges.append((indices_col[j], indices_line[i], bipartie[i][j]))
        #ort_mat[indices_col[j]][indices_line[i]] = bipartie[i][j]
                
    return euler_edges, predecessor