import random

from Logic.Field import Field
from Logic.Ship import Ship


class Game:
    def __init__(self):
        self.start_game()

    def start_game(self) -> None:
        self.field_gamer = Field()
        self.field_comp = Field()
        self.ships_gamer = self.create_ships()
        self.ships_comp = self.create_ships()
        self.__count_ships_gamer = 10
        self.__count_ships_comp = 10
        self.queue = None

    def begin_game(self, auto: bool = True) -> None:
        if auto:
            self.__auto_set_ships_gamer()
        self.__auto_set_ships_comp()
        # Очерёдность хода: 1 - компьютер, 0 - игрок
        self.queue = random.randint(0, 1)

    def move(self, x: int, y: int, gamer: bool = False) -> (str, []):
        """
            Возвращает состояние хода, и клетки пораженные в случае уничтожения корабля
        """
        if gamer:
            result, cells = self.field_comp.shoot(x, y)
            if result == "destroyed":
                self.__count_ships_comp -= 1
            if self.__count_ships_comp == 0:
                return "gamer_win", []
            if result == "away":
                self.queue = 1
            return result, cells
        else:
            result, cells = self.field_gamer.shoot(x, y)
            if result == "destroyed":
                self.__count_ships_gamer -= 1
            if self.__count_ships_gamer == 0:
                return "computer_win", []
            if result == "away":
                self.queue = 0
            return result, cells

    def create_ships(self) -> []:
        ship1 = [Ship(1), Ship(1), Ship(1), Ship(1)]
        ship2 = [Ship(2), Ship(2), Ship(2)]
        ship3 = [Ship(3), Ship(3)]
        ship4 = [Ship(4)]
        return ship4 + ship3 + ship2 + ship1

    def __adjacent(self, cell: (), next_cell: ()) -> [()]:
        if cell[0] == next_cell[0]:
            if cell[1] < next_cell[1]:
                return [(cell[0], cell[1] - 1), (next_cell[0], next_cell[1] + 1)]
            else:
                return [(cell[0], cell[1] + 1), (next_cell[0], next_cell[1] - 1)]
        else:
            if cell[0] < next_cell[0]:
                return [(cell[0] - 1, cell[1]), (next_cell[0] + 1, next_cell[1])]
            else:
                return [(cell[0] + 1, cell[1]), (next_cell[0] - 1, next_cell[1])]

    def __generate_coord(self, field: Field, ship: Ship):
        cells = [key for key, value in field.items() if value.status == "open"]
        while True:
            cell = random.choice(cells)
            result = [cell]

            if ship.decks == 1:
                return result

            adjacent = [(cell[0] + 1, cell[1]), (cell[0] - 1, cell[1]), (cell[0], cell[1] - 1), (cell[0], cell[1] + 1)]
            next_cells = [elem for elem in adjacent if elem in cells]

            if not next_cells:
                continue

            next_cell = random.choice(next_cells)
            result.append(next_cell)

            if ship.decks == 2:
                return result

            adjacent = self.__adjacent(cell, next_cell)
            next_cells = [elem for elem in adjacent if elem in cells]

            if not next_cells:
                continue

            next_cell = random.choice(next_cells)
            result.append(next_cell)

            if ship.decks == 3:
                return result

            if cell[0] == next_cell[0]:
                result = sorted(result, key=lambda x: x[1])
            else:
                result = sorted(result, key=lambda x: x[0])

            adjacent = self.__adjacent(result[0], result[-1])
            next_cells = [elem for elem in adjacent if elem in cells]

            if not next_cells:
                continue

            next_cell = random.choice(next_cells)
            result.append(next_cell)

            return result

    def set_ship(self, num_ship: int, cells: [()]) -> bool:
        self.field_gamer, status = self.ships_gamer[num_ship].set_ship(self.field_gamer, cells)
        return status

    def __auto_set_ships_comp(self) -> None:
        for ship in self.ships_comp:
            self.field_comp, _ = ship.set_ship(self.field_comp, self.__generate_coord(self.field_comp, ship))

    def __auto_set_ships_gamer(self) -> None:
        for ship in self.ships_gamer:
            self.field_gamer, _ = ship.set_ship(self.field_gamer, self.__generate_coord(self.field_gamer, ship))
