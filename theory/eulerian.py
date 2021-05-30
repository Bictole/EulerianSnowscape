from scipy.optimize import linear_sum_assignment
from theory.graph import is_edge_connected, odd_vertices, is_edge_connected_weighted, odd_vertices_weighted, single_source_distances
import numpy as np
import math
import time
import sys

from theory.tools import *

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

def is_eulerian_weighted(n, edges):
    return is_edge_connected_weighted(n, edges) and not odd_vertices_weighted(n, edges)

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
            return cycle[0:-1]
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
    sum_col,sum_line = compute_degrees(ort_mat)
    surcharge, souscharge = compute_charge(sum_line,sum_col,n)
      
    bipartie = []
    indices_line = []
    indices_col = []
    dist = []
    start_time = time.time()
    count = 0
    for j in range(n):
        if j in surcharge:
            dist.append(single_source_distances(n, edges, j))
            # Display process status
            count += 1
            percent = (count / len(surcharge)) * 100
            compute_time = time.time() - start_time
            time_left = compute_time * (len(surcharge) - count) / count
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
        ort_mat[indices_col[j]][indices_line[i]] = bipartie[i][j]
                
    return ort_mat