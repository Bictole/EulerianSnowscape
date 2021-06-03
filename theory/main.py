from theory.tools import mat_to_edges
from theory.eulerian import find_eulerian_cycle, find_eulerian_cycle_weighted_v2, is_eulerian_weighted, make_eulerian
from theory.graph import make_connected, np_build_adj_mat_directed_weighted
from theory.oriented_edge import orient_graph
from theory.print_tools import print_graph_with_weights

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted

def main(n, edges):
    #print_graph_with_weights(n,edges)
    mat = np_build_adj_mat_directed_weighted(n,edges)
    #mat = make_connected(n, mat)
    oriented_mat = orient_graph(n, mat)
    oriented_edges = mat_to_edges(n, oriented_mat)
    print_graph_with_weights(n, oriented_edges)
    final_mat = make_eulerian(n, oriented_mat, edges)
    final_edges = mat_to_edges(n , final_mat)
    print(is_eulerian_weighted(n, final_edges))
    #print_graph_with_weights(n,final_edges)
    return find_eulerian_cycle_weighted_v2(n, mat_to_edges(n, final_mat))

    