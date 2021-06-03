from networkx.algorithms.shortest_paths.unweighted import predecessor
from theory.tools import mat_to_edges
from theory.eulerian import find_eulerian_cycle, find_eulerian_cycle_weighted, find_eulerian_cycle_weighted_custom, is_eulerian_weighted, make_eulerian
from theory.graph import make_connected, make_strongly_connected, np_build_adj_mat_directed_weighted
from theory.oriented_edge import orient_graph
from theory.print_tools import print_graph_with_weights

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted

def main(n, edges):
    mat = make_strongly_connected(n, edges)
    oriented_mat = orient_graph(n, mat)
    oriented_edges = mat_to_edges(n, oriented_mat)
    prev_len = len(oriented_edges)
    final_edges, predecessor= make_eulerian(n, oriented_mat, edges)

    print("Is the graph eulerian now ? ", is_eulerian_weighted(n, final_edges))
    path = find_eulerian_cycle_weighted_custom(n, final_edges, len(final_edges) - prev_len, predecessor)
    return path

    