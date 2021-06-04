from theory.drone import question_1_1
from theory.main import main
from application.city_tools import  city_to_edges_weighted, compute_time, print_route
import osmnx as ox
import osmnx.utils_graph as ox_utils

print("Démonstration sur la ville de Montréal (France)")

# Récupère les informations pour la ville de Montréal en France
city = ox.graph_from_place('Montréal, France', network_type='drive')

# Retire les noeuds qui ne permettent pas à la ville d'être strongly connected
city = ox_utils.get_largest_component(city, strongly=True)

print("Voici le plan de la ville à déneiger:")
ox.plot_graph(city)

## Drone

# Nombre d'intersection
n = city.number_of_nodes()
# Liste de tuples de format (u, v, w) avec u,v des sommets et w la longueur de l'arête (en mètre)
edges = city_to_edges_weighted(city)

path = question_1_1(n, edges)
print(path)
## Déneigeuse

# Nombre de déneigeuse en service
nb_split = 5
print("Nombre de déneigeuse utilisée:", nb_split)

# Vitesse moyenne d'une déneigeuse (en km/h)
speed = 40
print("Vitesse moyenne d'une déneigeuse:", speed, "km/h")

# Nombre d'intersection
n = city.number_of_nodes()
# Liste de tuples de format (u, v, w) avec u,v des sommets et w la longueur de l'arête (en mètre)
edges = city_to_edges_weighted(city)

# Algorithme principal, renvoit la liste des cycles à parcourir en fonction du nombre de déneigeuses
split_path = main(n , edges, nb_split)

# Calcule le temps estimée pour chaque cycle (en heures)
estimate_time = compute_time(n, edges, split_path, speed)

# Enregistre les itinéraires pour chaque déneigeuses dans des fichiers
print("Génération des itinéraires :")
print_route(n, city, split_path, estimate_time)
