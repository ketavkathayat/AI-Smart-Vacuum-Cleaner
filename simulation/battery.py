
from config import MAX_BATTERY, CLEAN_COST

from algorithms.astar import search


def get_return_path(environment, position):

    path, explored, cost = search(
        environment,
        position,
        environment.charging_station
    )

    return path, explored, cost


def required_battery(path_to_target, path_to_home):

    travel_cost = max(0, len(path_to_target) - 1)

    return_cost = max(0, len(path_to_home) - 1)

    return travel_cost + CLEAN_COST + return_cost


def recharge_vacuum(vacuum):

    while vacuum.battery < MAX_BATTERY:
        vacuum.recharge()

    vacuum.status = "Fully Charged"
