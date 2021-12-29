from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QAbstractGraphicsShapeItem

from Logic.Game import Game
from Logic.Strategy import Strategy


# Оставшиеся корабли
class RemainingShips:
    def __init__(self):
        self.current_num = 0
        self.items_ship = {}
        self.items = {(1, 10): None, (2, 10): None, (3, 10): None, (4, 10): None}
        self.current = [(1, 10), (2, 10), (3, 10), (4, 10)]
        self.ship1 = 4
        self.ship2 = 3
        self.ship3 = 2
        self.ship4 = 1

    # поворот коробля
    def rotate(self) -> [()]:
        if self.current_num < 6:
            current = sorted(self.current)
            cell = current[-2]
            sum_cell = cell[0] + cell[1]
            current = list(map(lambda x: (sum_cell - x[1], sum_cell - x[0]), current))

            min_y = min(current, key=lambda x: x[1])[1]
            min_x = min(current, key=lambda x: x[0])[0]
            max_x = max(current, key=lambda x: x[0])[0]
            max_y = max(current, key=lambda x: x[1])[1]

            delta = 0
            if min_y < 1:
                delta = min_y - 1
            elif max_y > 10:
                delta = max_y - 10
            if delta != 0:
                current = list(map(lambda x: (x[0], x[1] - delta), current))

            delta = 0
            if min_x < 1:
                delta = min_x - 1
            elif max_x > 10:
                delta = max_x - 10
            if delta != 0:
                current = list(map(lambda x: (x[0] - delta, x[1]), current))
            return sorted(current)


class Slots:
    def __init__(self, ui):
        self.ui = ui
        self.game = Game()
        self.strategy = Strategy()
        self.msg = QMessageBox()
        self.msg.setWindowIcon(QIcon("icon.ico"))
        self.hand_mode = False
        self.remaining_ships = None
        self.x = {1: "А", 2: "Б", 3: "В", 4: "Г", 5: "Д", 6: "Е", 7: "Ё", 8: "Ж", 9: "З", 10: "И"}

    # начало игры
    def start_game(self) -> None:
        # сюда надо установить вопрос
        self.game.start_game()
        self.strategy.start()
        self.ui.start_game.setVisible(False)
        self.ui.scene_gamer.clear()
        self.ui.scene_comp.clear()
        self.ui.protocol.clear()
        self.hand_mode = False
        self.remaining_ships = None
        for i in range(1, 5):
            self.ui.count_g[i - 1].setText(f"    - {5 - i}")
            self.ui.count_c[i - 1].setText(f"    - {5 - i}")
        self.__interactive(True)

    # начало партии
    def begin_game(self) -> None:
        if self.ui.auto.isChecked():
            self.game.begin_game()
            for coord, cell in self.game.field_gamer.items():
                if cell.status == "occupied":
                    self.ui.scene_gamer.draw_ship(coord[0], coord[1])
            self.__interactive(False)
            if self.game.queue == 1:
                self.ui.protocol.append("Компьютер начинает")
                self.__move_computer()
            else:
                self.ui.protocol.append("Игрок начинает")
            self.ui.start_game.setVisible(True)
        else:
            self.__instruction(True)
            self.hand_mode = True
            self.remaining_ships = RemainingShips()
            self.ui.scene_gamer.setFocus()
            for x, y in self.remaining_ships.current:
                _, item_ship = self.ui.scene_gamer.draw_ship(x, y)
                self.remaining_ships.items_ship[x, y] = item_ship
            self.__interactive(False)

    # отображение предварительных настроек
    def __interactive(self, state: bool) -> None:
        self.ui.lbl_ships_set.setVisible(state)
        self.ui.auto.setVisible(state)
        self.ui.hand.setVisible(state)
        self.ui.set_ships.setVisible(state)

    # передвинуть корабль вверх
    def up(self):
        if self.hand_mode:
            current = []
            items = {}
            items_ship = {}
            self.remaining_ships.current = sorted(self.remaining_ships.current, key=lambda x: x[1])
            if self.remaining_ships.current[0][1] > 1:
                for x, y in self.remaining_ships.current:
                    x_new, y_new = x, y - 1
                    current.append((x_new, y_new))
                    if (x_new, y_new) in self.ui.scene_gamer.items.keys():
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new, True)
                    else:
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new)

                    self.__remaining_items(x, y, x_new, y_new, items, items_ship, item, item_ship)
                self.__set_remaining(current, items_ship, items)

    # передвинуть корабль
    def __move_ship(self, border: int, delta_x: int = 0, delta_y: int = 0):
        pass

    # передвинуть корабль вниз
    def down(self):
        if self.hand_mode:
            current = []
            items = {}
            items_ship = {}
            self.remaining_ships.current = sorted(self.remaining_ships.current, key=lambda x: x[1], reverse=True)
            if self.remaining_ships.current[0][1] < 10:
                for x, y in self.remaining_ships.current:
                    x_new, y_new = x, y + 1
                    current.append((x_new, y_new))
                    if (x_new, y_new) in self.ui.scene_gamer.items.keys():
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new, True)
                    else:
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new)

                    self.__remaining_items(x, y, x_new, y_new, items, items_ship, item, item_ship)
                self.__set_remaining(current, items_ship, items)

    # передвинуть корабль влево
    def left(self):
        if self.hand_mode:
            current = []
            items = {}
            items_ship = {}
            self.remaining_ships.current = sorted(self.remaining_ships.current, key=lambda x: x[0])
            if self.remaining_ships.current[0][0] > 1:
                for x, y in self.remaining_ships.current:
                    x_new, y_new = x - 1, y
                    current.append((x_new, y_new))
                    if (x_new, y_new) in self.ui.scene_gamer.items.keys():
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new, True)
                    else:
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new)

                    self.__remaining_items(x, y, x_new, y_new, items, items_ship, item, item_ship)
                self.__set_remaining(current, items_ship, items)

    # передвинуть корабль вправо
    def right(self):
        if self.hand_mode:
            current = []
            items = {}
            items_ship = {}
            self.remaining_ships.current = sorted(self.remaining_ships.current, key=lambda x: x[0], reverse=True)
            if self.remaining_ships.current[0][0] < 10:
                for x, y in self.remaining_ships.current:
                    x_new, y_new = x + 1, y
                    current.append((x_new, y_new))
                    if (x_new, y_new) in self.ui.scene_gamer.items.keys():
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new, True)
                    else:
                        item, item_ship = self.ui.scene_gamer.draw_ship(x_new, y_new)

                    self.__remaining_items(x, y, x_new, y_new, items, items_ship, item, item_ship)
                self.__set_remaining(current, items_ship, items)

    # повернуть корабль
    def rotate(self):
        if self.hand_mode:
            num = self.remaining_ships.current_num
            if num < 6:
                current = self.remaining_ships.rotate()
                items = {}
                items_ship = {}
                ship = ()
                for (x, y) in current:
                    if (x, y) in self.remaining_ships.items_ship:
                        item_ship = self.remaining_ships.items_ship[(x, y)]
                        item = self.remaining_ships.items[(x, y)]
                        ship = (x, y)
                    elif (x, y) in self.ui.scene_gamer.items.keys():
                        item, item_ship = self.ui.scene_gamer.draw_ship(x, y, True)
                    else:
                        item, item_ship = self.ui.scene_gamer.draw_ship(x, y)
                    items_ship[(x, y)] = item_ship
                    items[(x, y)] = item

                for (x, y) in self.remaining_ships.current:
                    if (x, y) != ship:
                        self.__return_cell(x, y)
                self.__set_remaining(current, items_ship, items)

    # установить корабль
    def space(self):
        if self.hand_mode:
            status = self.game.set_ship(self.remaining_ships.current_num, self.remaining_ships.current)
            if status:
                self.remaining_ships.current_num += 1
                self.remaining_ships.items = {}
                self.remaining_ships.items_ship = {}

                if self.remaining_ships.current_num < 10:
                    if 1 <= self.remaining_ships.current_num < 3:
                        self.remaining_ships.current = [(1, 10), (2, 10), (3, 10)]
                    elif 3 <= self.remaining_ships.current_num < 6:
                        self.remaining_ships.current = [(1, 10), (2, 10)]
                    else:
                        self.remaining_ships.current = [(1, 10)]

                    # отрисовываем очередной корабль
                    for coord in self.remaining_ships.current:
                        if coord in self.ui.scene_gamer.items.keys():
                            self.remaining_ships.items[coord] = self.ui.scene_gamer.items[coord]
                            flag = True
                        else:
                            self.remaining_ships.items[coord] = None
                            flag = False
                        _, item_ship = self.ui.scene_gamer.draw_ship(coord[0], coord[1], flag)
                        self.remaining_ships.items_ship[coord] = item_ship
                # все корабли установлены
                else:
                    self.hand_mode = False
                    self.remaining_ships = None
                    self.ui.start_game.setVisible(True)
                    self.__instruction(False)
                    self.game.begin_game(False)
                    if self.game.queue == 1:
                        self.ui.protocol.append("Компьютер начинает")
                        self.__move_computer()
                    else:
                        self.ui.protocol.append("Игрок начинает")
            else:
                self.msg.setWindowTitle("Ошибка")
                self.msg.setText("Здесь нельзя установить корабль!")
                self.msg.show()

    # установить параметры очередного корабля
    def __set_remaining(self, current: [], items_ship: {}, items: {}) -> None:
        self.remaining_ships.current = current
        self.remaining_ships.items_ship = items_ship
        self.remaining_ships.items = items

    # удаляет корабль и добавляет на его место item который был до этого
    def __remaining_items(self, x: int, y: int, x_new: int, y_new: int, items: {},
                          items_ship: {}, item: QAbstractGraphicsShapeItem,
                          item_ship: QAbstractGraphicsShapeItem) -> None:
        items[x_new, y_new] = item
        items_ship[x_new, y_new] = item_ship
        self.__return_cell(x, y)

    # вернуть ячейку к состоянию до установки корабля
    def __return_cell(self, x: int, y: int) -> None:
        self.ui.scene_gamer.removeItem(self.remaining_ships.items_ship[x, y])
        self.ui.scene_gamer.items.pop((x, y), None)
        if self.remaining_ships.items[x, y]:
            old_item = self.remaining_ships.items[x, y]
            self.ui.scene_gamer.addItem(old_item)
            self.ui.scene_gamer.items[x, y] = old_item

    # надписи сообщающие о том как установить корабль
    def __instruction(self, state: bool) -> None:
        self.__interactive(state)
        self.ui.up.setVisible(state)
        self.ui.down.setVisible(state)
        self.ui.left.setVisible(state)
        self.ui.right.setVisible(state)
        self.ui.rotate.setVisible(state)
        self.ui.set_lbl.setVisible(state)

    # выстрел игрока
    def shoot(self) -> None:
        if self.game.queue is None:
            self.msg.setWindowTitle("Ошибка")
            self.msg.setText("Сначала нужно установить корабли!")
            self.msg.show()
        elif self.game.queue == 0:
            x = int(self.ui.scene_comp.x // 29) + 1
            y = int(self.ui.scene_comp.y // 29) + 1
            self.ui.scene_comp.x = None
            self.ui.scene_comp.y = None
            result, cells = self.game.move(x, y, True)
            if result == "amazed":
                self.ui.protocol.append(f"({y}, {self.x[x]}) - Игрок попал в корабль")
                self.ui.scene_comp.draw_ship(x, y, True)
            elif result == "destroyed":
                decks = self.game.field_comp[x, y].ship.decks
                count = int(self.ui.count_c[decks - 1].text()[-1]) - 1
                self.ui.count_c[decks - 1].setText(f"    - {count}")
                self.ui.protocol.append(f"({y}, {self.x[x]}) - Игрок уничтожил {decks}-палубный корабль")
                self.ui.scene_comp.draw_ship(x, y, True)
                self.ui.scene_comp.draw_loc_ship(cells)
            elif result == "away":
                self.ui.protocol.append(f"({y}, {self.x[x]}) - Игрок промахнулся")
                self.ui.scene_comp.draw_away(x, y)
                self.__move_computer()
            elif result == "gamer_win":
                decks = self.game.field_comp[x, y].ship.decks
                count = int(self.ui.count_c[decks - 1].text()[-1]) - 1
                self.ui.count_c[decks - 1].setText(f"    - {count}")
                self.ui.scene_comp.draw_ship(x, y, True)
                self.ui.protocol.append(f"({y}, {self.x[x]}) - Игрок уничтожил {decks}-палубный корабль")
                self.ui.protocol.append("Игрок выиграл!")
                self.game.queue = 1
                self.msg.setWindowTitle("Победа")
                self.msg.setText("Вы победили!😎")
                self.msg.show()

    # выстрел компьютера
    def __move_computer(self) -> None:
        def __shoot_computer():
            x, y = self.strategy.shoot()
            result, cells = self.game.move(x, y)
            self.strategy.analysis(x, y, result)
            return x, y, result, cells

        x, y, result, cells = __shoot_computer()
        while result != "away" and result != "computer_win":
            if result == "destroyed":
                decks = self.game.field_gamer[x, y].ship.decks
                count = int(self.ui.count_g[decks - 1].text()[-1]) - 1
                self.ui.count_g[decks - 1].setText(f"    - {count}")
                self.ui.protocol.append(f"({y}, {self.x[x]}) - Компьютер уничтожил {decks}-палубный корабль")
                self.ui.scene_gamer.draw_ship(x, y, True)
                self.ui.scene_gamer.draw_loc_ship(cells)
                for x, y in cells:
                    self.strategy.remove(x, y)
            elif result == "amazed":
                self.ui.protocol.append(f"({y}, {self.x[x]}) - Компьютер попал в корабль")
                self.ui.scene_gamer.draw_ship(x, y, True)

            x, y, result, cells = __shoot_computer()

        if result == "computer_win":
            decks = self.game.field_gamer[x, y].ship.decks
            count = int(self.ui.count_g[decks - 1].text()[-1]) - 1
            cells = sum([elem.cells for elem in self.game.ships_comp if elem.healthy > 0], [])
            heatly_cells = [elem for elem in cells if self.game.field_comp[elem].status == "occupied"]
            for cell in heatly_cells:
                self.ui.scene_comp.draw_ship(cell[0], cell[1])
            self.ui.count_g[decks - 1].setText(f"    - {count}")
            self.ui.scene_gamer.draw_ship(x, y, True)
            self.ui.protocol.append(f"({y}, {self.x[x]}) - Компьютер уничтожил {decks}-палубный корабль")
            self.ui.protocol.append("Компьютер выиграл!")
            self.msg.setWindowTitle("Поражение")
            self.msg.setText("Вы проиграли!😞")
            self.msg.show()
        else:
            self.ui.protocol.append(f"({y}, {self.x[x]}) - Компьютер промахнулся")
            self.ui.scene_gamer.draw_away(x, y)
