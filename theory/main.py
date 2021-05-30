from theory.tools import mat_to_edges
from theory.eulerian import find_eulerian_cycle, find_eulerian_cycle_weighted, make_eulerian
from theory.graph import make_connected, np_build_adj_mat_directed_weighted
from theory.oriented_edge import orient_graph

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted

def main(n, edges):
    #print_graph_with_weights(n,edges)
    mat = np_build_adj_mat_directed_weighted(n,edges)
    mat = make_connected(n, mat)
    oriented_mat = orient_graph(n, mat)
    final_mat = make_eulerian(n, oriented_mat, edges)
    print(final_mat)
    #print_graph_with_weights(n,mat_to_edges(n,final_mat))
    return find_eulerian_cycle_weighted(n, mat_to_edges(n, final_mat))

    