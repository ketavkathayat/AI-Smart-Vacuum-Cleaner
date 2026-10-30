
from agents.goal_agent import ALGORITHMS


def choose_target(environment, start, algorithm_name):

    algorithm = ALGORITHMS[algorithm_name]

    best_target = None
    best_path = []
    best_score = float("-inf")
    total_explored = 0

    for target in environment.dirty_areas:

        path, explored, cost = algorithm(
            environment, start, target
        )

        total_explored += explored

        if not path:
            continue

        dirt_level = environment.dirt_levels.get(
            target, 1
        )

        utility = (dirt_level * 10) / (cost + 1)

        if utility > best_score:

            best_score = utility
            best_target = target
            best_path = path

    return (
        best_target,
        best_path,
        total_explored,
        best_score
    )
