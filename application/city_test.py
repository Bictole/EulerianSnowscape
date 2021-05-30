#%%
import sys
sys.path.insert(0,"..")
from re import X
from networkx.classes.function import get_edge_attributes
from theory.graph import *
from theory.eulerian import *
from theory.main import main
from application.city_tools import *
import networkx as nx 
import osmnx as ox
import time
#%%
# Get the city graph (from OpenStreetMap), filter only the drive ways
city = ox.graph_from_place('Les Crottes, France', network_type='drive')
#%%
# Display the graph
ox.plot_graph(city)
#%%
print("City data:\n")
n = city.number_of_nodes()
edges = city_to_algo(city)
print("Number of nodes: ", city.number_of_nodes())
print("Number of edges: ", city.number_of_edges())
#print("List of all nodes: \n", city.nodes())
#print()
#print("List of all edges: \n", city.edges())
#print()
#print("Degree for all nodes: \n", dict(city.degree()))
#print()
# %%
# Get general degree for each nodes
degree = list(city.degree())
# Get in-degree for each nodes
in_degree = list(city.in_degree())
# Get out-degree for each nodes
out_degree = list(city.out_degree())
# %%
# Drone path computation
# path = question_1_1(len(city), edges)
#%%
# Final city test
start_time = time.time()
print(main(city.number_of_nodes(), edges))
print("Time: ", time.time() - start_time)
#%%
