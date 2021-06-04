#%%
from theory.graph import np_build_adj_mat_directed_weighted
import osmnx as ox
# Adapt the graph to our algorithm
def city_to_edges_weighted(city):
    city_to_algo = {}
    nb = 0
    for n in city.nodes():
        city_to_algo[n] = nb
        nb += 1

    edges = []
    for n1, n2, data in city.edges(data=True):
        edges.append((city_to_algo[n1], city_to_algo[n2], int(data['length'])))
    return edges

def city_to_edges_names(city):
    city_to_algo = {}
    nb = 0
    for n in city.nodes():
        city_to_algo[n] = nb
        nb += 1

    edges = []
    for n1, n2, data in city.edges(data=True):
        try:
            edges.append((city_to_algo[n1], city_to_algo[n2], data['name']))
        except KeyError:
            edges.append((city_to_algo[n1], city_to_algo[n2], "undefined"))
    return edges

def city_to_coords(city):
    nb = 0
    nodes = [(0, 0)] * city.number_of_nodes()
    for n , data in city.nodes(data=True):
        nodes[nb] = (data['x'], data['y'])
        nb += 1
    return nodes 

def print_snowplow_route(n, city, split_path, estimate_time):
    edges = city_to_edges_names(city)
    M = []
    for _ in range (0, n):
        M.append(["undefined"]*n)
    for u, v, name in edges:
        M[u][v] = name 

    for nb, path in enumerate(split_path):
        file = open("Itinéraire_déneigeuse_" + str(nb + 1) + ".txt", "w")
        file.write("Temps estimée: " +  str(estimate_time[nb]) + " heures\n")
        file.write("Départ déneigeuse " + str(nb + 1) + "\n")
        pos = path[0]
        name = ""
        for i in range(1, len(path)):
            if name != M[pos][path[i]] and M[pos][path[i]] != "undefined":
                name = M[pos][path[i]]
                file.write("-> " + str(M[pos][path[i]]) + "\n")
            pos = path[i]
        file.write("Arrivé dénéigeuse "+ str(nb + 1) + "\n")
        print(file.name + ": Done")
        file.close()

def print_drone_route(n, city, path, nodes_coords):
    file = open("Itinéraire_drone.txt", "w")
    file.write("Départ drone\n")
    for i in range(0, len(path)):
        file.write("-> " + str(nodes_coords[path[i]]) + "\n")
    
    file.write("Arrivé drone\n")
    print(file.name + ": Done")
    file.close()

def compute_time(n, edges, split_path, speed):
    mat = np_build_adj_mat_directed_weighted(n ,edges)
    estimate_time = []
    for path in split_path:
        pos = path[0]
        total_weight = 0
        for i in range(1, len(path)):
            total_weight += mat[pos][path[i]]
            pos = path[i]
        estimate_time.append((total_weight / 1000) / speed)
    return estimate_time

#%%