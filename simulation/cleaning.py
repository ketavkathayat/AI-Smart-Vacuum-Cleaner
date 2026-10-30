
def clean_current_area(environment, vacuum):

    position = vacuum.position

    if position not in environment.dirty_areas:
        return False

    if vacuum.clean():

        environment.clean_area(position)

        return True

    return False


def cleaning_completed(environment):

    return len(environment.dirty_areas) == 0
