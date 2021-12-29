import random


class Strategy:
    def __init__(self):
        self.start()

    def start(self) -> None:
        self.open_cell = [(i, j) for i in range(1, 11) for j in range(1, 11)]
        self.review_list = []
        self.prev_shot = None

    def shoot(self) -> ():
        if not self.review_list:
            return random.choice(self.open_cell)
        else:
            shot = random.choice(self.review_list)
            self.review_list.remove(shot)
            return shot

    def remove(self, x: int, y: int) -> None:
        if (x, y) in self.open_cell:
            self.open_cell.remove((x, y))

    def analysis(self, x: int, y: int, status: str) -> None:
        if status == "destroyed":
            self.review_list = []
            self.prev_shot = None
        elif status == "amazed":
            if self.prev_shot is None:
                adjacent = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
                self.review_list = [elem for elem in adjacent if elem in self.open_cell]
            else:
                if self.prev_shot[0] == x:
                    self.review_list = [elem for elem in self.review_list if elem[0] == x]
                    if self.prev_shot[1] < y:
                        next = (x, y + 1) if (x, y + 1) in self.open_cell else None
                    else:
                        next = (x, y - 1) if (x, y - 1) in self.open_cell else None
                    if next is not None:
                        self.review_list.append(next)
                else:
                    self.review_list = [elem for elem in self.review_list if elem[1] == y]
                    if self.prev_shot[0] < x:
                        next = (x + 1, y) if (x + 1, y) in self.open_cell else None
                    else:
                        next = (x - 1, y) if (x - 1, y) in self.open_cell else None
                    if next is not None:
                        self.review_list.append(next)
            self.prev_shot = (x, y)
        self.remove(x, y)
