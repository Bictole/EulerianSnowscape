import enum
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
    sum_line = np.sum(mat, axis=1)
    for i in range(n):
        if sum_line[i] == 0:
            index, val = get_smallest_not_zero(mat[:,i])
            mat[i][index] = val
            sum_line = np.sum(mat, axis=1)
    return mat

def scc(n, edges):
    # Convert to adjacency list
    succ = [[] for _ in range(n)]
    for (s,d,w) in edges:
        succ[s].append(d)
    # Dijkstra-based SCC enumeration, using a live stack as in Tarjan
    # 
    # Since only a single pass of the automaton is necessary, we will destroy
    # the adjacency list as the DFS processes the edges, this way we only need to
    # keep a stack of states.
    inscc = [None] * n  # the number of the SCC containing each state

    scc.n = 0 # the number of SCCs discovered so far 
 
    index = [0] * n  # discovery index of each vertex
    scc.next_index = 1
    
    def dfs(s):
        stack = [s]
        live = [s]
        index[s] = scc.next_index
        roots = [scc.next_index]
        scc.next_index += 1
        while stack:
            src = stack[-1]
            if len(succ[src]) == 0:  # all successors processed, backtrack
                stack.pop()
                if index[src] == roots[-1]:
                    # Unwind the live stack.  
                    # All vertices until src belong to the same SCC.
                    while True:
                        x = live.pop()
                        inscc[x] = scc.n
                        if x == src:
                            break
                    scc.n += 1
                    roots.pop()
            else: # we have one successor
                dst = succ[src].pop()
                idst = index[dst]
                if idst > 0:  # a previously visited vertex 
                    if inscc[dst] is None: # but not yet in a known SCC
                        # pop all roots greater that idst
                        while roots[-1] > idst:
                            roots.pop()
                else: # a new vertex
                    index[dst] = scc.next_index
                    roots.append(scc.next_index)
                    scc.next_index += 1
                    stack.append(dst)
                    live.append(dst)
    for s in range(n):
        if inscc[s] is None:
            dfs(s)
    return inscc, scc.n

def make_strongly_connected(n, edges):
    composantes, nb_composantes = scc(n, edges)
    mat = np_build_adj_mat_directed_weighted(n, edges)
    if nb_composantes == 1:
        return mat
    seen = [False] * nb_composantes 
    for index, comp in enumerate(composantes):
        if False not in seen:
            break
        if not seen[comp]:
            find = False
            for succ, weight in enumerate(mat[index]):
                if weight and composantes[succ] != comp:
                    mat[succ][index] = weight
                    edges.append((succ, index, weight))
                    find = True
                    break
            if find:
                continue
            for pred, weight in enumerate(mat[:,index]):
                if weight and composantes[pred] != comp:
                    mat[index][pred] = weight
                    edges.append((index, pred, weight))
                    find = True
                    break
    return mat