#%%
# Adapt the graph to our algorithm
def city_to_algo(city):
    city_to_algo = {}

    nb = 0
    for n in city.nodes():
        city_to_algo[n] = nb
        nb += 1

    edges = []
    for n1, n2, data in city.edges(data=True):
        edges.append((city_to_algo[n1], city_to_algo[n2], int(data['length'])))
    return edges
#%%