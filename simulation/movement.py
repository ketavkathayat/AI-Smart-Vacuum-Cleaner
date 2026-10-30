
def move_one_step(environment, vacuum, next_position):

    if not environment.is_valid(next_position):
        return False

    if vacuum.battery < 1:
        vacuum.status = "Low Battery"
        return False

    return vacuum.move(next_position)


def execute_path(environment, vacuum, path):

    if not path:
        return False

    for position in path[1:]:

        success = move_one_step(
            environment,
            vacuum,
            position
        )

        if not success:
            return False

        vacuum.path.append(position)

    return True
