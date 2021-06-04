from networkx.algorithms.shortest_paths.unweighted import predecessor
from theory.tools import mat_to_edges
from theory.eulerian import find_eulerian_cycle, find_eulerian_cycle_weighted, find_eulerian_cycle_weighted_custom, is_eulerian_weighted, make_eulerian
from theory.graph import split_path, get_path_cumulate_weight, make_connected, make_strongly_connected, np_build_adj_mat_directed_weighted
from theory.oriented_edge import orient_graph
from theory.print_tools import print_graph_with_weights

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.shortest_paths import weighted

def main(n, edges, nb_split):

    if not is_eulerian_weighted(n, edges):
        print("Le graphe est-il eulérien de base ?", is_eulerian_weighted(n, edges))
    # Rend le graphe strongly connected 
    mat = make_strongly_connected(n, edges)

    # Rend le graphe orienté
    oriented_mat = orient_graph(n, mat)
    oriented_edges = mat_to_edges(n, oriented_mat)

    prev_len = len(oriented_edges)
    # Rend le graphe eulérien
    final_edges, predecessor= make_eulerian(n, oriented_mat, edges)

    print("Le graphe est-il eulérien ?", is_eulerian_weighted(n, final_edges))

    # Récupère le cycle eulérien en prenant en compte l'ajout précédent des arêtes, 
    # c'est à dire en prenant en compte le plus court chemins pour se rendre d'un point à un autre
    path = find_eulerian_cycle_weighted_custom(n, final_edges, len(final_edges) - prev_len, predecessor)

    # Calcule les poids cumulés au fur et à mesure du cycle eulérien
    cumulate_weight = get_path_cumulate_weight(n, edges, path)

    # Découpe le path en plusieurs paths de poids équivalent en 
    # incluant le point de départ et le retour en fonction du nombre nb_split
    path_split = split_path(path, cumulate_weight, nb_split)
    return path_split, cumulate_weight

    