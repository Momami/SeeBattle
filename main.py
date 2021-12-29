import sys

from PyQt5 import QtWidgets

from Interface.MainWindow import MainWindow
from Interface.Slots import RemainingShips

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    sys.exit(app.exec_())
