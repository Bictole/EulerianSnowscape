#%%
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted
from theory.graph import build_adj_mat

# Some print tools
def print_graph(edges):
    G = nx.MultiDiGraph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True,connectionstyle='arc3, rad = 0.1')
    return G , pos

# Create a dictionnary (key = edge, value = order in the path) 
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
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    G = nx.MultiDiGraph()
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, width=2, connectionstyle='arc3, rad = 0.1')
    labels = nx.get_edge_attributes(G,'weight')
    weight_labels = {}
    for a in labels:
        weight_labels[(a[0], a[1])] = labels[a]
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight_labels)
    plt.savefig("graph.png", dpi=1000)
    return G , pos
# %%