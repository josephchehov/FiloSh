import sys
from terminal import Window
from PySide6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setCursorFlashTime(700)

    widget = Window()
    widget.show()

    sys.exit(app.exec())