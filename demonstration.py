from osmnx.simplification import consolidate_intersections
from theory.drone import question_1_1
from theory.main import main
from application.city_tools import  city_to_coords, city_to_edges_weighted, compute_time, print_drone_route, print_snowplow_route
import osmnx as ox
import osmnx.utils_graph as ox_utils

print("Démonstration sur la ville de Montréal (France)")

# Récupère les informations pour la ville de Montréal en France
city = ox.graph_from_place('Montréal, France', network_type='drive')

# Retire les noeuds qui ne permettent pas à la ville d'être strongly connected
city = ox_utils.get_largest_component(city, strongly=True)

ox.plot_graph(city)

## Drone

# Nombre d'intersection
n = city.number_of_nodes()
# Liste de tuples de format (u, v, w) avec u,v des sommets et w la longueur de l'arête (en mètre)
edges = city_to_edges_weighted(city)

# Calcule du cycle eulérien pour le drone
path = question_1_1(n, edges)

# Récupération des coordonnées de chaques sommets
nodes_coords = city_to_coords(city)

# Enregistre l'itinéraire du drone dans un fichier
print("Génération de l'itinéraire du drone:")
print_drone_route(n, city, path, nodes_coords)
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
print()
split_path, cumulate_weight = main(n , edges, nb_split)

# Calcule le temps estimée pour chaque cycle (en heures)
estimate_time = compute_time(n, edges, split_path, speed)

# Enregistre les itinéraires pour chaque déneigeuses dans des fichiers
print()
print("Génération des fichiers d'itinéraires des déneigeuses:")
print_snowplow_route(n, city, split_path, estimate_time)

print()
total_weight = cumulate_weight[len(cumulate_weight) -1] 
print("Distance totale du chemin:", total_weight / 1000, "km")

prix_carburant = 1.24
consomation_carburant = 30
carburant_total = int(prix_carburant * consomation_carburant / 100 * total_weight / 1000)
print("Coût du carburants des déneigeuses", carburant_total, "€")

cout_de_location = 400
location_total = int(cout_de_location * (total_weight / 1000) / speed) * nb_split
print("Coût de location des déneigeuses", location_total, "€")

print("Coût total: ", carburant_total + location_total, "€")