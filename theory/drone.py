# %%
from theory.graph import odd_vertices, is_eulerian, find_eulerian_cycle
# Make the graph eulerian with drone conditions
def drone_make_eulerian(n, edges):
    odd_degree = odd_vertices(n, edges)
    for i in range(0, len(odd_degree) - 1, 2):
        edges.append((odd_degree[i+1], odd_degree[i]))
                
# Compute the path for the drone
def question_1_1(n, edges):
    if not is_eulerian(n, edges):
        drone_make_eulerian(n, edges)
        assert is_eulerian(n, edges)
    return find_eulerian_cycle(n, edges)