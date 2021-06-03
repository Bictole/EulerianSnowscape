
#%%
# Test make_connected
from theory.eulerian import is_eulerian_weighted, make_eulerian
from theory.graph import make_connected, np_build_adj_mat_directed_weighted


n = 2
bad_edges = [(0,1,2)]
mat = np_build_adj_mat_directed_weighted(n , bad_edges)
print(mat)
print(make_connected(n , mat))

#%%
import theory.print_tools as pt
from theory.oriented_edge import orient_graph
from theory.graph import *
from theory.eulerian import *
from theory.tools import *
# Test make_eulerian
n = 4
#edges = [(0,1,3),(0,2,11),(1,2,5),(2,3,1),(2,1,5), (1,0,3)]
#edges = [(0,1,1),(1, 0,2), (0,2,3), (2, 0, 4)]
edges = [(0,1,1), (1,0,2), (0,2,3),(2,0,4),(3,2,5),(2,3,6)]
oriented_edges = [(0,1,1), (0,2,3),(3,2,5)]
pt.print_graph(edges)
#%%
mat = np_build_adj_mat_directed_weighted(n, edges)
orient_mat = orient_graph(n,mat)
oriented_mat = np_build_adj_mat_directed_weighted(n, oriented_edges)
print(oriented_mat)
euler_mat = make_eulerian(n, oriented_mat, edges)
print(euler_mat)
edges = mat_to_edges(n, euler_mat)
print(is_eulerian_weighted(n, edges))
pt.print_graph(edges)
#%%
'''
G = nx.Graph()


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

#print(add_edges(3, [(0,1,4),(1,2,3)]))
#print(add_edges(4, [(0,1,1),(0,2,1),(0,3,1)]))
#print(make_eulerian_great_again(9,[(0,1,3),(1,2,5),(1,5,4),(2,4,2),(2,3,4),(5,4,5),(5,6,3),(4,8,4),(4,6,6),(6,7,3),(8,6,4), (2,1,5),(4,2,2),(5,1,4),(6,4,6),(7,6,3),(5,0,7),(3,2,4)]))

    #print(add_edges(4,[(0,1,3),(0,2,11),(1,2,5),(2,3,1),(3,0,3)]))    
#print(add_edges(7, [(0, 1, 11), (0, 4, 3), (0, 5, 7), (0, 6, 5), (1, 2, 11), (2, 3, 11), (3, 0, 11), (4, 3, 1), (5, 2, 5), (6, 1, 3)]))    
        
#main(4, [(0,1,3),(0,2,11),(1,2,5),(2,3,1),(3,0,3), (0,3,3), (2,1,5), (1,0,3)])
#print_graph_with_weights(3,[(0,1,1),(1,2,1),(2,0,1),(0,2,1)])
#print(flow_graph(3,[(0,1),(1,2),(2,0),(0,2)]))
'''