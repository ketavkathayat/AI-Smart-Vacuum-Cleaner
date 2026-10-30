
from environment import Environment

from algorithms import bfs
from algorithms import dfs
from algorithms import ucs
from algorithms import greedy
from algorithms import astar


# Create house environment

env = Environment()

start = env.start
goal = env.charging_station


# Algorithms

algorithms = {
    "BFS": bfs.search,
    "DFS": dfs.search,
    "UCS": ucs.search,
    "Greedy Best First": greedy.search,
    "A*": astar.search
}


print("\nAI VACUUM CLEANER - SEARCH ALGORITHM TEST")

print("Start Position:", start)
print("Goal Position:", goal)

print("-" * 50)


for name, algorithm in algorithms.items():

    path, explored, cost = algorithm(
        env, start, goal
    )

    print("\nAlgorithm:", name)

    print("Path:", path)

    print("Nodes Explored:", explored)

    print("Path Cost:", cost)

    print("Path Found:", bool(path))

    print("-" * 50)
