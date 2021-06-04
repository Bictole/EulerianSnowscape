from networkx.algorithms.shortest_paths.unweighted import predecessor
from numpy import unsignedinteger
from theory.main import main
from application.city_tools import   city_to_edges_weighted, compute_time, print_snowplow_route
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
        speed = int(input("Entrez la vitesse moyenne (km/h) d'une déneigeuse: "))
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

prix_carburant = 0
while True:
    try:
        prix_carburant = float(input("Entrez le prix en carburant d'une déneigeuse: "))
        if prix_carburant < 0:
            print("Veuillez entrer un nombre positif !")
            continue
        break
    except ValueError:
        print("Veuillez entrer un nombre valide !")

consomation_carburant = 0
while True:
    try:
        consomation_carburant = int(input("Entrez la consomation en carburant (L/100km) d'une déneigeuse: "))
        if consomation_carburant < 0:
            print("Veuillez entrer un nombre positif !")
            continue
        break
    except ValueError:
        print("Veuillez entrer un nombre valide !")

carburant_total = int(prix_carburant * consomation_carburant / 100 * total_weight / 1000)
print("Coût du carburants des déneigeuses", carburant_total, "€")

cout_de_location = 0
while True:
    try:
        cout_de_location= int(input("Entrez le coût de location à l'heure d'une déneigeuse: "))
        if cout_de_location < 0:
            print("Veuillez entrer un nombre positif !")
            continue
        break
    except ValueError:
        print("Veuillez entrer un nombre valide !")

location_total = int(cout_de_location * (total_weight / 1000) / speed) * nb_split
print("Coût de location des déneigeuses", location_total, "€")

print("Coût total: ", carburant_total + location_total, "€")