#%%
import networkx as nx
G = nx.Graph()
  
edges = [(1, 2, 19), (1, 6, 15), (2, 3, 6), (2, 4, 10), 
         (2, 6, 22), (3, 4, 51), (3, 5, 14), (4, 8, 20),
         (4, 9, 42), (6, 7, 30)]
  
G.add_weighted_edges_from(edges)
# %%

# %%
pos = nx.spring_layout(G, seed=2)

p = nx.shortest_path(G,1,3)
for e in G.edges():
    G[e[0]][e[1]]['color'] = 'black'
for i in range(len(p)-1):
    G[p[i]][p[i+1]]['color'] = 'dark_red'
edge_color_list = [ G[e[0]][e[1]]['color'] for e in G.edges() ]
nx.draw(G, pos, with_labels = True, edge_color=edge_color_list)

# %%

# %%
def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]

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

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

def find_eulerian_cycle(n, edges):
    assert is_eulerian(n, edges)
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
# %%