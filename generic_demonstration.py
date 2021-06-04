from networkx.algorithms.shortest_paths.unweighted import predecessor
from numpy import unsignedinteger
from theory.graph import get_path_total_weight
from theory.main import main
from application.city_tools import  city_to_edges_names, city_to_edges_weighted, compute_time, print_route
import osmnx as ox
import osmnx.utils_graph as ox_utils


while True:
    try:
        city_name = input("Entrez la ville que vous souhaitez déneiger: ")
        city_country = input("Entrez son pays: ")
        city = ox.graph_from_place(city_name + ", " + city_country , network_type='drive')
        break
    except ValueError:
        print("Aucune ville ne correspond au couple pays/ville fourni !")

# Retire les noeuds qui ne permettent pas à la ville d'être strongly connected
city = ox_utils.get_largest_component(city, strongly=True)

print("Voici le plan de la ville à déneiger:")
ox.plot_graph(city)

# Nombre de déneigeuse en service
nb_split = 0
while True:
    try:
        nb_split = int(input("Entrez le nombre de déneigeuse en service: "))
        if nb_split < 0:
            print("Veuillez entrer un nombre positif !")
            continue
        break
    except ValueError:
        print("Veuillez entrer un nombre valide !")

# Vitesse moyenne d'une déneigeuse (en km/h)
speed = 0
while True:
    try:
        speed = int(input("Entrez la vitesse moyenne d'une déneigeuse: "))
        if speed < 0:
            print("Veuillez entrer un nombre positif !")
            continue
        break
    except ValueError:
        print("Veuillez entrer un nombre valide !")


# Nombre d'intersection
n = city.number_of_nodes()
# Liste de tuples de format (u, v, w) avec u,v des sommets et w la longueur de l'arête (en mètre)
edges = city_to_edges_weighted(city)

# Algorithme principal, renvoit la liste des cycles à parcourir en fonction du nombre de déneigeuses
split_path = main(n , edges, nb_split)

# Calcule le temps estimée pour chaque cycle (en heures)
estimate_time = compute_time(n, edges, split_path, speed)

# Enregistre les itinéraires pour chaque déneigeuses dans des fichiers
print_route(n, city, split_path, estimate_time)

