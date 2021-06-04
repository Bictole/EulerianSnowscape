# %%
from theory.graph import odd_vertices_weighted
from theory.eulerian import find_eulerian_cycle_weighted, is_eulerian_unoriented_weighted

# Make the graph eulerian with drone conditions
def drone_make_eulerian(n, edges):
    odd_degree = odd_vertices_weighted(n, edges)
    for i in range(0, len(odd_degree) - 1, 2):
        edges.append((odd_degree[i+1], odd_degree[i], 1))
                

# Compute the path for the drone
def question_1_1(n, edges):
    if not is_eulerian_unoriented_weighted(n, edges):
        drone_make_eulerian(n, edges)
        assert is_eulerian_unoriented_weighted(n, edges)
    return find_eulerian_cycle_weighted(n, edges)

