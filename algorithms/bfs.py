
from collections import deque

from algorithms.common import (
    get_neighbors,
    reconstruct_path
)


def search(environment, start, goal):

    queue = deque([start])

    visited = {start}

    parent = {start: None}

    explored = 0

    while queue:

        current = queue.popleft()

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

                queue.append(neighbor)

    return [], explored, float("inf")
