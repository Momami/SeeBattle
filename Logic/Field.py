class Field(dict):
    def __init__(self):
        super().__init__({(i, j): Cell() for i in range(12) for j in range(12)})
        for i in range(12):
            self[i, 0].status = "blocked"
            self[i, 11].status = "blocked"
            self[0, i].status = "blocked"
            self[11, i].status = "blocked"

    def shoot(self, x, y) -> (str, []):
        """
            Возвращает статус выстрела, и клетки пораженые вокруг, в случае уничтножения корабля
            is_hit - клетка уже поражена
            away - выстрел поразил пустую клетку
            amazed - выстрел поразил клетку с кораблём
            destroyed - выстрел уничтожил корабль
        """
        status = self[x, y].status
        if status == "hit" or status == "hit_ship":
            return "is_hit", []
        if status == "occupied":
            self[x, y].ship.healthy -= 1
            self[x, y].status = "hit_ship"
            if self[x, y].ship.healthy == 0:
                return "destroyed", self[x, y].ship.shoot(self)
            return "amazed", []
        else:
            self[x, y].status = "hit"
            return "away", []


class Cell:
    """
        состояния клетки:
            open - открыта
            blocked - заблокирована
            occupied - установлен корабль
            hit - поражена
            hit_ship - поражена
    """

    def __init__(self):
        self.status = "open"
        self.ship = None
