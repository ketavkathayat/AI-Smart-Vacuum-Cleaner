
import heapq
from itertools import count

from algorithms.common import (
    get_neighbors,
    manhattan_distance,
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

    visited = {start}

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

            return path, explored, len(path) - 1

        for neighbor in get_neighbors(
            current, environment
        ):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                heuristic = manhattan_distance(
                    neighbor, goal
                )

                heapq.heappush(
                    priority_queue,
                    (
                        heuristic,
                        next(counter),
                        neighbor
                    )
                )

    return [], explored, float("inf")
