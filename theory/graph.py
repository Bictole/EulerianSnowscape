import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.cuts import edge_expansion
import numpy as np
import math
from networkx.algorithms.shortest_paths import weighted

def adjlist(n, edges, directed=False):
    lst = [[] for _ in range(n)]
    for (s,d, w) in edges:
        lst[s].append(d)
        if not directed:
            lst[d].append(s)
    return lst

def build_adj_mat_undirected(n, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        M[edge[0]][edge[1]] = 1
        M[edge[1]][edge[0]] = 1
    return M

def build_adj_mat_directed(n, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        M[edge[0]][edge[1]] = 1
    return M

def build_adj_mat_directed_weighted(n, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        M[edge[0]][edge[1]] = edge[2]
    return M

def np_build_adj_mat_directed_weighted(n, edges):
    M = np.full((n,n), 0)
    for edge in edges:
        M[edge[0]][edge[1]] = edge[2]
    return M

def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def odd_vertices_weighted(n, edges):
    deg = [0] * n
    for (a,b,w) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

def check_balance_degree(n, edges):
    in_degree = [0] * n
    out_degree = [0] * n
    for (a, b, w) in edges:
        out_degree[a] += 1
        in_degree[b] += 1
    return [i for i in range(n) if in_degree[i] - out_degree[i] != 0]

def degree_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return deg

def in_degree_vertices(n, edges):
    in_degree = [0] * n
    for (a, b) in edges:
        in_degree[b] += 1
    return in_degree

def out_degree_vertices(n, edges):
    out_degree = [0] * n
    for (a, b ) in edges:
        out_degree[a] += 1
    return out_degree

def is_edge_connected(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b) in edges:
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

def is_edge_connected_weighted(n, edges):
    if n == 0 or len(edges) == 0:
        return True
    # Convert to adjacency list
    succ = [[] for a in range(n)]
    for (a,b, w) in edges:
        succ[a].append(b)
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

def single_source_distances(n,edges,src):
    # Classic Bellman-Ford for directed graphs
    dist = [math.inf] * n
    dist[src] = 0
    for k in range(n - 1):
        for (s, d, w) in edges:
            dist[d] = min(dist[d], dist[s] + w)
    return dist

def all_pairs_shortest_path(n, cost):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if cost[i][k] + cost[k][j] < cost[i][j]:
                    cost[i][j] = cost[i][k] + cost[k][j]
    return cost
def get_smallest_not_zero(L):
    index = np.argmax(L)
    for j in range(len(L)):
        if L[j] > 0 and L[j] < L[index]:
            index = j
    return index, L[index]

def make_connected(n, mat):
    sum_col = np.sum(mat, axis=0)
    for i in range(n):
        if sum_col[i] == 0:
            index, val = get_smallest_not_zero(mat[i])
            mat[index][i] = val
            sum_col = np.sum(mat, axis=0)
    return mat