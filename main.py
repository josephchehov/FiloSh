import sys
import random
from terminal import Window
from PySide6 import QtCore, QtWidgets, QtGui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Window()
    widget.show()

    sys.exit(app.exec())