from copy import copy, deepcopy

from Logic.Field import Field


class Ship:
    def __init__(self, count):
        self.decks = count
        self.healthy = count
        self.cells = []

    def check(self, field: Field, cells: [()]) -> (Field, bool):
        l = len(set(cells))
        x = set(map(lambda x: x[0], cells))
        y = set(map(lambda x: x[1], cells))

        if l != self.decks or (len(x) != 1 and len(y) != 1):
            return field, False

        x_min = min(cells, key=lambda coord: coord[0])[0]
        x_max = max(cells, key=lambda coord: coord[0])[0]
        y_min = min(cells, key=lambda coord: coord[1])[1]
        y_max = max(cells, key=lambda coord: coord[1])[1]

        if x_min < 1 or x_max > 10 or y_min < 1 or y_max > 10:
            return field, False

        if x_max - x_min >= self.decks or y_max - y_min >= self.decks:
            return field, False

        field_temp = deepcopy(field)

        for x, y in cells:
            if field_temp[x, y].status != "open":
                return field, False
            field_temp[x, y].status = "occupied"
            field_temp[x, y].ship = self
            self.cells = cells
        return field_temp, True

    def shoot(self, field: Field) -> []:
        """
            Возвращает список пораженых клеток вокруг корабля
        """
        shot = []
        x_min = min(self.cells, key=lambda coord: coord[0])[0] - 1
        x_max = max(self.cells, key=lambda coord: coord[0])[0] + 2
        y_min = min(self.cells, key=lambda coord: coord[1])[1] - 1
        y_max = max(self.cells, key=lambda coord: coord[1])[1] + 2
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                if field[x, y].status == "blocked":
                    shot.append((x, y))
                    field[x, y].status = "hit"
        return shot

    def set_ship(self, field: Field, cells: [()]) -> (Field, bool):
        field_temp, check_state = self.check(field, cells)
        if not check_state:
            return field, False
        x_min, x_max = min(cells, key=lambda coord: coord[0])[0] - 1, max(cells, key=lambda coord: coord[0])[0] + 2
        y_min, y_max = min(cells, key=lambda coord: coord[1])[1] - 1, max(cells, key=lambda coord: coord[1])[1] + 2
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                if field_temp[x, y].status != "occupied":
                    field_temp[x, y].status = "blocked"
                    field_temp[x, y].ship = None
        return field_temp, True
