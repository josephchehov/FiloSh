import sys
from PySide6.QtCore import Qt, QPoint
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

class Titlebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(30)

        icon = QtGui.QIcon("images/icon.png")
        icon_pixmap = icon.pixmap(QtCore.QSize(30,30))
        self.app_icon = QLabel()
        self.app_icon.setPixmap(icon_pixmap)
        self.app_icon.setContentsMargins(5,0,0,0)

        self.title_label = QLabel("FILOSH")
        self.title_label.setStyleSheet("font-weight: bold; font-family: Segou UI; font-size: 13px;")
        self.title_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.title_label.setContentsMargins(5,0,0,0)

        self.version_label = QLabel("ver 1.0")
        self.version_label.setStyleSheet("font-weight: bold; color: #454545;")
        self.version_label.setContentsMargins(5,0,0,0)
        
        self.minimize_button = QPushButton()
        self.maximize_button = QPushButton()
        self.close_button = QPushButton()
        self.minimize_button.setIcon(QtGui.QIcon("images/minimize.png"))
        self.maximize_button.setIcon(QtGui.QIcon("images/maximize.png"))
        self.close_button.setIcon(QtGui.QIcon("images/close.png"))
        
        for btn in (self.minimize_button, self.maximize_button, self.close_button):
            btn.setFixedSize(30,30)
            
        self.minimize_button.setStyleSheet("""
            QPushButton {background-color: #363636; color: black; border: none;}
            QPushButton:hover {background-color: #313030;}
        """)

        self.maximize_button.setStyleSheet("""
            QPushButton {background-color: #363636; color: black; border: none;}
            QPushButton:hover {background-color: #313030;}
        """)

        self.close_button.setStyleSheet("""
            QPushButton {background-color: #363636; color: black; border: none; border-top-right-radius: 10px;}
            QPushButton:hover {background-color: #8F0D00; border-top-right-radius: 10px;}
        """)
        
        self.minimize_button.clicked.connect(self.parent.showMinimized)
        self.maximize_button.clicked.connect(self.toggle_max_restore)
        self.close_button.clicked.connect(self.parent.close)

        #- adding
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.app_icon)
        layout.addWidget(self.title_label)
        layout.addWidget(self.version_label)
        layout.addStretch()
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
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QColor("#363636"))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
    
        rect = QtCore.QRectF(0, 0, self.width(), self.height() + 10)
        painter.drawRoundedRect(rect, 10, 10)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(700,450)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.titlebar = Titlebar(self)
        layout.addWidget(self.titlebar)

        content = QLabel("Placeholder")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(content)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        rect = QtCore.QRectF(self.rect())
        painter.setBrush(QtGui.QColor("#1e1e1e"))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 10, 10)