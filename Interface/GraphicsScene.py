from PyQt5.QtCore import pyqtSignal, Qt, QLineF, QRectF
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent


class GraphicsScene(QGraphicsScene):
    click_for_show_coord = pyqtSignal()
    click_up = pyqtSignal()
    click_down = pyqtSignal()
    click_right = pyqtSignal()
    click_left = pyqtSignal()
    click_rotate = pyqtSignal()
    click_set = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = {}
        self.draw_lines()

    def draw_lines(self):
        pen_for_lines = QPen(Qt.darkMagenta)
        for i in range(29, 290, 29):
            self.addLine(QLineF(i, 0, i, 290), pen_for_lines)
            self.addLine(QLineF(0, i, 290, i), pen_for_lines)

    def draw_ship(self, x: int, y: int, shot: bool = False) -> []:
        rect = QRectF((x - 1) * 29, (y - 1) * 29, 29, 29)
        item = None
        if shot:
            brush = QBrush(Qt.red)
        else:
            brush = QBrush(Qt.black)
        if (x, y) in self.items.keys():
            item = self.items[(x, y)]
            self.removeItem(item)
        brush.setStyle(Qt.Dense4Pattern)
        self.items[(x, y)] = self.addRect(rect, brush=brush)
        return item, self.items[(x, y)]

    def draw_away(self, x: int, y: int):
        brush = QBrush(Qt.black)
        if (x, y) in self.items.keys():
            self.removeItem(self.items[(x, y)])
        self.addEllipse((x - 1) * 29 + 10, (y - 1) * 29 + 10, 9, 9, brush=brush)

    def draw_loc_ship(self, cells: [()]):
        for x, y in cells:
            if 10 >= x >= 1 and 10 >= y >= 1:
                self.draw_away(x, y)

    def clear(self) -> None:
        super().clear()
        self.items = {}
        self.draw_lines()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.x = event.scenePos().x()
        self.y = event.scenePos().y()
        self.click_for_show_coord.emit()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        up = 16777235
        down = 16777237
        left = 16777234
        right = 16777236
        space = 32
        ctrl = 16777249
        key = event.key().numerator
        if key == up:
            self.click_up.emit()
        if key == down:
            self.click_down.emit()
        if key == left:
            self.click_left.emit()
        if key == right:
            self.click_right.emit()
        if key == space:
            self.click_set.emit()
        if key == ctrl:
            self.click_rotate.emit()
