#%%

from re import X
from theory.graph import *
from theory.eulerian import *
import osmnx as ox
import time
import sys

# %%

#%%
# Get the city graph (from OpenStreetMap), filter only the drive ways
city = ox.graph_from_place('Montreal, Canada', network_type='drive')
#%%
#%%
# Display the graph
ox.plot_graph(city)
#%%

#%%


#%%
import networkx as nx 

print("Number of nodes: ", city.number_of_nodes())
print("Number of edges: ", city.number_of_edges())
print("List of all nodes: \n", city.nodes())
print()
print("List of all edges: \n", city.edges())
print()
print("Degree for all nodes: \n", dict(city.degree()))
print()


# %%

#%%
a = city.nodes().get(4492648682)
#%%

# %%
# Get general degree for each nodes
degree = list(city.degree())
# Get in-degree for each nodes
in_degree = list(city.in_degree())
# Get out-degree for each nodes
out_degree = list(city.out_degree())

# %%

# %%
# Adapt the graph to our algorithm
city_to_algo = {}
algo_to_city = {}

nb = 0
for n in city.nodes():
    city_to_algo[n] = nb
    algo_to_city[nb] = n
    nb += 1

edges = []
for e in city.edges():
    edges.append((city_to_algo[e[0]], city_to_algo[e[1]]))

#%%
#%%
print(len(edges))
print(is_eulerian(len(city), edges))
naive_make_eulerian(odd_vertices(len(city), edges), edges)
print(is_eulerian(len(city), edges))
print(len(edges))
# %%
#%%
path = question_1_1(len(city), edges)
# %%

#%%
start_time = time.time()
if len(edges[0]) == 2:
    edges = [(a, b, 0) for (a, b) in edges]
print(make_eulerian_great_again(city.number_of_nodes(), edges))
print("Time: ", time.time() - start_time)
#%%