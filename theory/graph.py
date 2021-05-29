#%%
import networkx as nx
from networkx.algorithms.shortest_paths import weighted

def print_graph(edges):
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True,connectionstyle='arc3, rad = 0.1')
    return G , pos

def get_labels_from_path(n , edges, path):
    nb = 1
    pos = path[0]
    mat = build_adj_mat(n, edges)
    edges_labels = {}
    for i in range(1, len(path)):
        j = 0
        if edges_labels.get((pos, path[i])):
            edges_labels[(pos, path[i])] = edges_labels.get((pos, path[i])) + '-' + str(nb)
        if edges_labels.get((path[i], pos)):
            edges_labels[(path[i], pos)] = edges_labels.get((path[i], pos)) + '-' + str(nb)
        else:
            edges_labels[(pos, path[i])] = str(nb) 
        pos = path[i]
        nb += 1
    edges_labels[(path[len(path) - 1], path[0])] = nb
    return edges_labels

def print_graph_with_labels(n, edges, path):
    G , pos = print_graph(edges)
    edges_labels = get_labels_from_path(n, edges, path)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges_labels)

def print_graph_with_weights(n, edges):
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from(edges)
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True,connectionstyle='arc3, rad = 0.1')
    labels = nx.get_edge_attributes(G,'weight')
    weight_labels = {}
    for a in labels:
        weight_labels[(a[0], a[1])] = labels[a]
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)
    return G , pos



# %%
def adjlist(n, edges, directed=False):
    lst = [[] for _ in range(n)]
    for (s,d) in edges:
        lst[s].append(d)
        if not directed:
            lst[d].append(s)
    return lst

def build_adj_mat(n, edges):
    M = []
    for i in range (0, n):
        M.append([0]*n)
    for edge in edges:
        M[edge[0]][edge[1]] = 1
        M[edge[1]][edge[0]] = 1
    return M

def odd_vertices(n, edges):
    deg = [0] * n
    for (a,b) in edges:
        deg[a] += 1
        deg[b] += 1
    return [a for a in range(n) if deg[a] % 2]


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

def is_eulerian(n, edges):
    return is_edge_connected(n, edges) and not odd_vertices(n, edges)

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

# %%
def naive_make_eulerian(odd_degree , edges):
    for i in range(0, len(odd_degree) - 1, 2):
        edges.append((odd_degree[i+1], odd_degree[i]))

#%%
def make_eulerian(n , edges):
    odd_degree = odd_vertices(n, edges)
    M = build_adj_mat(n, edges)
    seen = [False] * len(odd_degree)
    alone = []
    for k in range(len(odd_degree)):
        i = odd_degree[k]
        if (seen[k]):
            continue
        for l in range(len(odd_degree)):
            j = odd_degree[l]
            if (seen[l] or (i == j and j != len(odd_degree) - 1)):
                continue
    
            if (M[i][j]):
                edges.append((j,i))
                seen[k], seen[l] = True, True
                break

            if (j == len(odd_degree) - 1):
                alone.append(i)
    naive_make_eulerian(alone, edges)
                
def no_seen_make_eulerian(n ,edges):
    odd_degree = odd_vertices(n, edges)
    degree = degree_vertices(n, edges)
    M = build_adj_mat(n, edges)
    alone = []
    for k in range(len(odd_degree)):
        i = odd_degree[k]
        if degree[i] % 2 == 0:
            continue
        for l in range(len(odd_degree)):
            j = odd_degree[l]
            if i == j and j != len(odd_degree) - 1:
                continue
            if (M[i][j]):
                edges.append((j,i))
                degree[i] += 1
                degree[j] += 1
                break
            if (j == len(odd_degree) - 1):
                alone.append(i)
    naive_make_eulerian(alone, edges)
                
def question_1_1_1(n, edges):
    if not is_eulerian(n, edges):
        make_eulerian(n, edges)
        assert is_eulerian(n, edges)
    print("Start")
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

def question_1_1(n, edges):
    if not is_eulerian(n, edges):
        make_eulerian(n, edges)
        assert is_eulerian(n, edges)
    l = adjlist(n, edges)
    loc = 0
    for i in range(len(l)):
        if len(l[i]) != 0:
            loc = i
            break
    cycle = []
    stack = [loc]
    while stack:
        if len(l[loc]) == 0:
            cycle.append(loc)
            loc = stack.pop()
            continue
        stack.append(l[loc][0])
        oldloc = loc
        loc = l[loc][0]
        l[oldloc].remove(loc)
        l[loc].remove(oldloc)
    cycle.pop(0)
    return cycle

#%%
#%%
G = nx.Graph()

n = 6
bad_edges = [(0,1),(0,2),(0,3),(0,4),(1,2),(3,1),(4,1),(3,2),(2,4),(4,3),(4,5)]

path = question_1_1(n,bad_edges)
print_graph_with_labels(n, bad_edges, path)
#for e in G.edges():
#    G[e[0]][e[1]]['color'] = 'black'
#for i in range(len(p)-1):
#    G[p[i]][p[i+1]]['color'] = 'red'
#edge_color_list = [ G[e[0]][e[1]]['color'] for e in G.edges() ]

#%%
# Make eulerian edge case
# TEST 1
make_eulerian_test = [(0, 1), (0, 2), (0, 3)]

no_seen_make_eulerian(4, make_eulerian_test)
print_graph(make_eulerian_test)
print(make_eulerian_test)
#%%

# %%
# TEST 2
make_eulerian_test2 = [(0,2), (1,3), (2,3), (3, 4), (4, 2)]
print_graph(make_eulerian_test2)

# %%
no_seen_make_eulerian(5, make_eulerian_test2)
print_graph(make_eulerian_test2)
print(make_eulerian_test2)
# %%
# TEST 3
test3 = [(0, 1), (0,2), (0,3), (3,4), (3,5), (3,6)]
print_graph(test3)
#%%
#%%
no_seen_make_eulerian(7, test3)
print_graph(test3)
print(test3)
# %%

# %%
weighted_edges = [(0, 1, 3), (0,2, 4), (0,3, -1), (3,4, 2), (3,5, 4), (3,6, 1)]
print_graph_with_weights(7, weighted_edges)

# %%
