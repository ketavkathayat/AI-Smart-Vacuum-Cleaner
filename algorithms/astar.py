
import heapq
from itertools import count

from algorithms.common import (
    get_neighbors,
    manhattan_distance,
    calculate_step_cost,
    reconstruct_path
)


def search(environment, start, goal):

    counter = count()

    priority_queue = [
        (
            manhattan_distance(start, goal),
            next(counter),
            start
        )
    ]

    g_score = {start: 0}

    parent = {start: None}

    explored = 0

    while priority_queue:

        _, _, current = heapq.heappop(
            priority_queue
        )

        explored += 1

        if current == goal:

            path = reconstruct_path(
                parent, start, goal
            )

            return path, explored, g_score[current]

        for neighbor in get_neighbors(
            current, environment
        ):

            new_cost = (
                g_score[current]
                + calculate_step_cost(
                    neighbor, environment
                )
            )

            if new_cost < g_score.get(
                neighbor, float("inf")
            ):

                g_score[neighbor] = new_cost

                parent[neighbor] = current

                heuristic = manhattan_distance(
                    neighbor, goal
                )

                total_cost = new_cost + heuristic

                heapq.heappush(
                    priority_queue,
                    (
                        total_cost,
                        next(counter),
                        neighbor
                    )
                )

    return [], explored, float("inf")
