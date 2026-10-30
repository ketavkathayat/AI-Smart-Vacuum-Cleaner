
from config import MAX_BATTERY, MOVE_COST, CLEAN_COST, CHARGE_RATE


class VacuumState:

    def __init__(self, start_position):

        self.position = start_position
        self.battery = MAX_BATTERY

        self.distance_travelled = 0
        self.nodes_explored = 0
        self.cleaning_time = 0
        self.total_cleaned = 0

        self.status = "Idle"
        self.path = []

    def move(self, new_position):

        if self.battery >= MOVE_COST:

            self.position = new_position
            self.battery -= MOVE_COST

            self.distance_travelled += 1
            self.cleaning_time += 1

            self.status = "Moving"
            return True

        self.status = "Low Battery"
        return False

    def clean(self):

        if self.battery >= CLEAN_COST:

            self.battery -= CLEAN_COST
            self.total_cleaned += 1
            self.cleaning_time += 2

            self.status = "Cleaning"
            return True

        self.status = "Low Battery"
        return False

    def recharge(self):

        if self.battery < MAX_BATTERY:

            self.battery = min(
                MAX_BATTERY,
                self.battery + CHARGE_RATE
            )

            self.status = "Charging"
