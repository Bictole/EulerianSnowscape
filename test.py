#%%

import osmnx as ox
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

print("Number of nodes: ",len(city))
print("Number of edges: ", len(city.edges()))
print("List of all nodes: \n", city.nodes())
print()
print("List of all edges: \n", city.edges())
print()
print("Degree for all nodes: \n", dict(city.degree()))
print()

# %%
