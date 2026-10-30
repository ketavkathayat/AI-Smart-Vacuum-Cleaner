
from algorithms.common import (
    get_neighbors,
    reconstruct_path
)


def search(environment, start, goal):

    stack = [start]

    visited = {start}

    parent = {start: None}

    explored = 0

    while stack:

        current = stack.pop()

        explored += 1

        if current == goal:

            path = reconstruct_path(
                parent, start, goal
            )

            return path, explored, len(path) - 1

        neighbors = get_neighbors(
            current, environment
        )

        for neighbor in reversed(neighbors):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                stack.append(neighbor)

    return [], explored, float("inf")
