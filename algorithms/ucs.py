
import heapq
from itertools import count

from algorithms.common import (
    get_neighbors,
    calculate_step_cost,
    reconstruct_path
)


def search(environment, start, goal):

    counter = count()

    priority_queue = [
        (0, next(counter), start)
    ]

    cost_so_far = {start: 0}

    parent = {start: None}

    explored = 0

    while priority_queue:

        current_cost, _, current = heapq.heappop(
            priority_queue
        )

        if current_cost > cost_so_far[current]:
            continue

        explored += 1

        if current == goal:

            path = reconstruct_path(
                parent, start, goal
            )

            return path, explored, current_cost

        for neighbor in get_neighbors(
            current, environment
        ):

            new_cost = (
                current_cost
                + calculate_step_cost(
                    neighbor, environment
                )
            )

            if new_cost < cost_so_far.get(
                neighbor, float("inf")
            ):

                cost_so_far[neighbor] = new_cost

                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (
                        new_cost,
                        next(counter),
                        neighbor
                    )
                )

    return [], explored, float("inf")
