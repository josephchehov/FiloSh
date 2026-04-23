import sys
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

class Titlebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: grey;")

        self.title_label = QLabel("FiloSh")
        self.title_label.setStyleSheet("font-weight: bold;")
        self.title_label.setContentsMargins(10, 0, 0, 0)

        #-- temporary button icons
        self.minimize_button = QPushButton("-")
        self.maximize_button = QPushButton("#")
        self.close_button = QPushButton("x")

        for btn in (self.minimize_button, self.maximize_button, self.close_button):
            btn.setFixedSize(30,30)
            btn.setStyleSheet("""
                            QPushButton{
                                background-color: grey;
                                color: black;
                                border: None;
                            }
                            QPushButtonHover{
                                background-color: grey;
                            }
                            """)
        
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_max_restore)
        self.close_button.clicked.connect(self.parent.close)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.title_label)
        layout.stretch(1)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

        #- title bar position controllers
        self.start_pos = None
        self.dragging = False

    def toggle_max_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.childAt(event.pos()) in (self.title_label, None):
                self.start_pos = event.globalPosition().toPoint()
                self.dragging = True
            else:
                self.dragging = False
    
    def mouseMoveEvent(self, event):
        if self.start_pos and event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent.move(self.parent.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setMinimumSize(700,450)
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.titlebar = Titlebar(self)
        layout.addWidget(self.titlebar)

        content = QLabel("Hello this is a test")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content)