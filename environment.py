
import random
from config import GRID_SIZE


class Environment:

    def __init__(self):

        self.size = GRID_SIZE

        self.start = (7, 7)
        self.charging_station = (1, 1)

        self.obstacles = set()
        self.dirty_areas = set()
        self.dirt_levels = {}
        self.cleaned_areas = set()

        self.create_house()

    def create_house(self):

        for row in [4, 9]:

            for col in range(self.size):

                if col not in [2, 7, 12]:
                    self.obstacles.add((row, col))

        furniture = [
            (2, 5), (2, 6),
            (3, 5), (3, 6),
            (6, 10), (6, 11),
            (7, 10), (7, 11),
            (11, 3), (11, 4),
            (12, 3), (12, 4),
            (12, 9), (13, 9)
        ]

        self.obstacles.update(furniture)

        self.generate_dirt(12)

    def is_valid(self, position):

        row, col = position

        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and position not in self.obstacles
        )

    def generate_dirt(self, count=1):

        available = [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.is_valid((r, c))
            and (r, c) != self.start
            and (r, c) != self.charging_station
            and (r, c) not in self.dirty_areas
        ]

        amount = min(count, len(available))

        new_dirt = random.sample(available, amount)

        self.dirty_areas.update(new_dirt)

        for position in new_dirt:
            self.dirt_levels[position] = random.randint(1, 5)

    def clean_area(self, position):

        if position in self.dirty_areas:

            self.dirty_areas.remove(position)

            self.cleaned_areas.add(position)

            self.dirt_levels.pop(position, None)

            return True

        return False

    def add_obstacle(self, position):

        if (
            self.is_valid(position)
            and position != self.start
            and position != self.charging_station
            and position not in self.dirty_areas
        ):

            self.obstacles.add(position)

            return True

        return False
