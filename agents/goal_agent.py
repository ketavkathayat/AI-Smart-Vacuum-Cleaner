
from algorithms import bfs, dfs, ucs, greedy, astar


ALGORITHMS = {
    "BFS": bfs.search,
    "DFS": dfs.search,
    "Uniform Cost Search": ucs.search,
    "Greedy Best-First Search": greedy.search,
    "A*": astar.search
}


def choose_target(environment, start, algorithm_name):

    algorithm = ALGORITHMS[algorithm_name]

    best_target = None
    best_path = []
    best_cost = float("inf")
    total_explored = 0

    for target in environment.dirty_areas:

        path, explored, cost = algorithm(
            environment, start, target
        )

        total_explored += explored

        if path and cost < best_cost:

            best_target = target
            best_path = path
            best_cost = cost

    return (
        best_target,
        best_path,
        total_explored,
        best_cost
    )
