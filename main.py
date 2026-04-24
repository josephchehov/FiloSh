import sys
from terminal import Window
from PySide6 import QtWidgets, QtCore

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Window()
    widget.show()

    sys.exit(app.exec())