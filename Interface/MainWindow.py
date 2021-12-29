from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import *

from Interface.Slots import Slots
from Interface.GraphicsScene import GraphicsScene


class MainWindow():
    def __init__(self):
        self.central_widget = QWidget()
        self.main_grid_layout = QGridLayout(self.central_widget)
        self.slots = Slots(self)

        self.scene_gamer = GraphicsScene()
        self.scene_comp = GraphicsScene()
        self.view_gamer = QGraphicsView(self.scene_gamer)
        self.view_comp = QGraphicsView(self.scene_comp)

        self.protocol = QTextEdit()

        self.interactive = QGroupBox(self.central_widget)
        self.lbl_ships_set = QLabel(self.interactive)
        self.start_game = QCommandLinkButton(self.interactive)
        self.auto = QRadioButton(self.interactive)
        self.hand = QRadioButton(self.interactive)
        self.set_ships = QCommandLinkButton(self.interactive)
        self.up = QLabel(self.interactive)
        self.down = QLabel(self.interactive)
        self.left = QLabel(self.interactive)
        self.right = QLabel(self.interactive)
        self.rotate = QLabel(self.interactive)
        self.set_lbl = QLabel(self.interactive)

        self.ships = QGroupBox(self.central_widget)
        self.count_g = [QLabel(self.ships) for i in range(4)]
        self.count_c = [QLabel(self.ships) for i in range(4)]

        self.font = QFont()
        self.font.setPixelSize(18)

        self.initUi()

    def initUi(self):
        self.central_widget.setFixedSize(1050, 580)
        self.central_widget.setWindowIcon(QIcon("icon.ico"))
        self.central_widget.setWindowTitle("Морской бой")
        self.protocol.setReadOnly(True)
        self.create_fields()
        self.main_grid_layout.addWidget(self.protocol, 1, 2, 16, 1)
        self.create_footer()
        self.create_interactive()
        self.stat_ships()
        self.connection()
        self.central_widget.show()

    def create_footer(self):
        name_gamer = QGroupBox(self.central_widget)
        name_comp = QGroupBox(self.central_widget)
        name_protocol = QGroupBox(self.central_widget)

        lbl_gamer = QLabel(name_gamer)
        lbl_comp = QLabel(name_comp)
        lbl_protocol = QLabel(name_protocol)

        lbl_gamer.setFixedWidth(350)
        lbl_gamer.setText("Поле Игрока")
        lbl_gamer.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        lbl_gamer.setFont(self.font)
        lbl_comp.setFixedWidth(350)
        lbl_comp.setText("Поле Противника")
        lbl_comp.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        lbl_comp.setFont(self.font)
        lbl_protocol.setFixedWidth(300)
        lbl_protocol.setText("Протокол")
        lbl_protocol.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        lbl_protocol.setFont(self.font)

        self.main_grid_layout.addWidget(name_gamer, 0, 0, 1, 1)
        self.main_grid_layout.addWidget(name_comp, 0, 1, 1, 1)
        self.main_grid_layout.addWidget(name_protocol, 0, 2, 1, 1)

    def create_fields(self):
        self.scene_gamer.setSceneRect(0, 0, 290, 290)
        self.scene_comp.setSceneRect(0, 0, 290, 290)
        self.view_gamer.setFixedSize(292, 292)
        self.view_comp.setFixedSize(292, 292)

        field_gamer = QGroupBox(self.central_widget)
        field_comp = QGroupBox(self.central_widget)

        lbl_num_gamer = QLabel()
        lbl_char_gamer = QLabel()
        lbl_num_gamer.setText("1\n2\n3\n4\n5\n6\n7\n8\n9\n10")
        lbl_char_gamer.setText("  А   Б   В   Г   Д   Е   Ё   Ж   З   И")

        fontH = QFont()
        fontH.setPixelSize(20)
        fontV = QFont()
        fontV.setPixelSize(24)

        lbl_num_gamer.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        lbl_char_gamer.setFont(fontH)
        lbl_num_gamer.setFont(fontV)

        field_gamer.setFixedSize(350, 350)
        lay_gamer = QGridLayout(field_gamer)

        lay_gamer.addWidget(lbl_char_gamer, 0, 1, 1, 8)
        lay_gamer.addWidget(lbl_num_gamer, 1, 0, 8, 1)
        lay_gamer.addWidget(self.view_gamer, 1, 1, 8, 8)

        field_comp.setFixedSize(350, 350)
        lay_comp = QGridLayout(field_comp)

        lbl_num_comp = QLabel()
        lbl_char_comp = QLabel()
        lbl_num_comp.setText("1\n2\n3\n4\n5\n6\n7\n8\n9\n10")
        lbl_char_comp.setText("  А   Б   В   Г   Д   Е   Ё   Ж   З   И")
        lbl_num_comp.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        lbl_char_comp.setFont(fontH)
        lbl_num_comp.setFont(fontV)

        lay_comp.addWidget(lbl_char_comp, 0, 1, 1, 8)
        lay_comp.addWidget(lbl_num_comp, 1, 0, 8, 1)
        lay_comp.addWidget(self.view_comp, 1, 1, 8, 8)

        self.main_grid_layout.addWidget(field_gamer, 1, 0, 12, 1)
        self.main_grid_layout.addWidget(field_comp, 1, 1, 12, 1)

    def create_interactive(self):
        lay = QGridLayout(self.interactive)
        self.start_game.setFixedHeight(50)
        self.lbl_ships_set.setText("Установить корабли")
        self.lbl_ships_set.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.auto.setText("Автоматически")
        self.auto.setChecked(True)
        self.hand.setText("Вручную")
        self.set_ships.setText("Начать установку")

        self.auto.setFont(self.font)
        self.hand.setFont(self.font)
        self.lbl_ships_set.setFont(self.font)

        lay.addWidget(self.lbl_ships_set, 0, 0, 1, 2)
        lay.addWidget(self.auto, 1, 0, 1, 1)
        lay.addWidget(self.hand, 1, 1, 1, 1)
        lay.addWidget(self.set_ships, 2, 0, 1, 2)

        self.start_game.setText("Начать новую игру")
        lay.addWidget(self.start_game, 1, 0, 1, 2)
        self.start_game.setVisible(False)

        self.up.setText("↑ - Вверх")
        self.down.setText("↓ - Вниз")
        self.left.setText("← - Влево")
        self.right.setText("→ - Вправо")
        self.rotate.setText("ctrl - Повернуть")
        self.set_lbl.setText("space - Установить")
        self.up.setFont(self.font)
        self.down.setFont(self.font)
        self.left.setFont(self.font)
        self.right.setFont(self.font)
        self.rotate.setFont(self.font)
        self.set_lbl.setFont(self.font)
        self.up.setVisible(False)
        self.down.setVisible(False)
        self.left.setVisible(False)
        self.right.setVisible(False)
        self.rotate.setVisible(False)
        self.set_lbl.setVisible(False)
        lay.addWidget(self.up, 0, 0, 1, 1)
        lay.addWidget(self.down, 0, 1, 1, 1)
        lay.addWidget(self.left, 1, 0, 1, 1)
        lay.addWidget(self.right, 1, 1, 1, 1)
        lay.addWidget(self.rotate, 2, 0, 1, 1)
        lay.addWidget(self.set_lbl, 2, 1, 1, 1)

        self.main_grid_layout.addWidget(self.interactive, 13, 0, 4, 1)

    def stat_ships(self):
        for i in range(1, 5):
            self.count_g[i - 1].setText(f"    - {5 - i}")
            self.count_g[i - 1].setFont(self.font)
            self.count_c[i - 1].setText(f"    - {5 - i}")
            self.count_c[i - 1].setFont(self.font)

        lay = QGridLayout(self.ships)
        title = QLabel(self.ships)
        title.setText("Корабли")
        title.setFont(self.font)
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        ship4 = QPixmap()
        ship4.load("4-палубник.png")
        ship4g = QLabel(self.ships)
        ship4g.setPixmap(ship4)
        ship4c = QLabel(self.ships)
        ship4c.setPixmap(ship4)

        ship3 = QPixmap()
        ship3.load("3-палубник.png")
        ship3g = QLabel(self.ships)
        ship3g.setPixmap(ship3)
        ship3c = QLabel(self.ships)
        ship3c.setPixmap(ship3)

        ship2 = QPixmap()
        ship2.load("2-палубник.png")
        ship2g = QLabel(self.ships)
        ship2g.setPixmap(ship2)
        ship2c = QLabel(self.ships)
        ship2c.setPixmap(ship2)

        ship1 = QPixmap()
        ship1.load("1-палубник.png")
        ship1g = QLabel(self.ships)
        ship1g.setPixmap(ship1)
        ship1c = QLabel(self.ships)
        ship1c.setPixmap(ship1)

        lay.addWidget(title, 0, 0, 1, 4)
        lay.addWidget(ship4g, 1, 0, 1, 1)
        lay.addWidget(ship4c, 1, 2, 1, 1)
        lay.addWidget(self.count_g[3], 1, 1, 1, 1)
        lay.addWidget(self.count_c[3], 1, 3, 1, 1)
        lay.addWidget(ship3g, 2, 0, 1, 1)
        lay.addWidget(ship3c, 2, 2, 1, 1)
        lay.addWidget(self.count_g[2], 2, 1, 1, 1)
        lay.addWidget(self.count_c[2], 2, 3, 1, 1)
        lay.addWidget(ship2g, 3, 0, 1, 1)
        lay.addWidget(ship2c, 3, 2, 1, 1)
        lay.addWidget(self.count_g[1], 3, 1, 1, 1)
        lay.addWidget(self.count_c[1], 3, 3, 1, 1)
        lay.addWidget(ship1g, 4, 0, 1, 1)
        lay.addWidget(ship1c, 4, 2, 1, 1)
        lay.addWidget(self.count_g[0], 4, 1, 1, 1)
        lay.addWidget(self.count_c[0], 4, 3, 1, 1)

        self.main_grid_layout.addWidget(self.ships, 13, 1, 4, 1)

    def connection(self):
        self.start_game.clicked.connect(self.slots.start_game)
        self.set_ships.clicked.connect(self.slots.begin_game)
        self.scene_comp.click_for_show_coord.connect(self.slots.shoot)
        self.scene_gamer.click_up.connect(self.slots.up)
        self.scene_gamer.click_down.connect(self.slots.down)
        self.scene_gamer.click_left.connect(self.slots.left)
        self.scene_gamer.click_right.connect(self.slots.right)
        self.scene_gamer.click_rotate.connect(self.slots.rotate)
        self.scene_gamer.click_set.connect(self.slots.space)
