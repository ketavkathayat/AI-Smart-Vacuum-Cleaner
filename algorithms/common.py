
def get_neighbors(position, environment):

    row, col = position

    possible_moves = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1)
    ]

    return [
        position
        for position in possible_moves
        if environment.is_valid(position)
    ]


def manhattan_distance(position, goal):

    return (
        abs(position[0] - goal[0])
        + abs(position[1] - goal[1])
    )


def calculate_step_cost(position, environment):

    # Normal movement cost
    cost = 1.0

    row, col = position

    # Small risk penalty near furniture
    adjacent = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1)
    ]

    nearby_obstacles = sum(
        1 for cell in adjacent
        if cell in environment.obstacles
    )

    cost += nearby_obstacles * 0.25

    return cost


def reconstruct_path(parent, start, goal):

    if goal != start and goal not in parent:
        return []

    path = []
    current = goal

    while current is not None:

        path.append(current)
        current = parent[current]

    path.reverse()

    return path
