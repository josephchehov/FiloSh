import time
import parser
import os
from PySide6.QtCore import Qt
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

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
        self.minimize_button.setToolTip("Minimize")
        self.maximize_button.setToolTip("Maximize")
        self.close_button.setToolTip("Close")
        
        for btn in (self.minimize_button, self.maximize_button, self.close_button):
            btn.setFixedSize(30,30)
            btn.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoMousePropagation)
            btn.installEventFilter(self)
            
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

        #- applying widgets on screen
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

        #- title bar movement
        self.start_pos = None
        self.dragging = False

    def toggle_max_restore(self):
        if self.parent.is_maximized:
            if self.parent.normal_geometry:
                self.parent.setGeometry(self.parent.normal_geometry)
            self.parent.is_maximized = False
            self.close_button.setStyleSheet("""
                QPushButton {background-color: #363636; color: black; border: none; border-top-right-radius: 10px;}
                QPushButton:hover {background-color: #8F0D00; border-top-right-radius: 10px;}
            """)
        else:
            self.parent.normal_geometry = self.parent.geometry()
            screen = QtWidgets.QApplication.screenAt(self.parent.pos())
            self.parent.setGeometry(screen.availableGeometry())
            self.parent.is_maximized = True
            self.close_button.setStyleSheet("""
                QPushButton {background-color: #363636; color: black; border: none; border-top-right-radius: 0px;}
                QPushButton:hover {background-color: #8F0D00; border-top-right-radius: 0px;}
            """)
        
        self.parent.update()
        self.update()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            child = self.childAt(event.pos())
            blocked = (self.maximize_button, self.minimize_button, self.close_button)

            button_area_start = self.minimize_button.x()
            if child not in blocked and event.pos().x() < button_area_start:
                self.start_pos = event.globalPosition().toPoint()
                self.dragging = True
            else:
                self.dragging = False
                self.start_pos = None
    
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

        if self.parent.is_maximized:
            painter.drawRect(QtCore.QRectF(0, 0, self.width(), self.height()))
        else:
            painter.drawRoundedRect(QtCore.QRectF(0, 0, self.width(), self.height()+10), 10, 10)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.parser = parser.command_parser()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(700,450)
        self.is_maximized = False
        self.normal_geometry = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.titlebar = Titlebar(self)
        layout.addWidget(self.titlebar)

        #- Input & Output
        self.output = QtWidgets.QTextEdit(readOnly=True)
        self.output.setStyleSheet("""
                                QTextEdit {
                                    background-color: #0F0F0F;
                                    color: white;
                                    border: 0px;
                                    padding-left: 30px;
                                    padding-right: 30px;
                                    padding-top: 10px;
                                    padding-bottom: 10px;
                                    font-family: Monoscape;
                                    font-size: 13px;
                                }
                            """)

        self.input_cmd = QtWidgets.QLineEdit()
        self.input_cmd.setStyleSheet("""
                                QLineEdit {
                                    background-color: black;
                                    color: white;
                                    outline:  none;
                                    border: 3px solid #1A1A1A;
                                    border-radius: 5px;
                                    padding-left: 12px;
                                    padding-right: 12px;
                                }
                                QLineEdit:focus {
                                    border: 3px solid #1A1A1A;
                                }
                            """)
        self.input_font = QtGui.QFont("Lucida Console, 18")
        self.input_font.setBold(False)
        self.input_cmd.setFont(self.input_font)
        self.input_cmd.setFixedHeight(48)
        self.input_cmd.setContentsMargins(15, 0, 15, 15)

        self.input_cmd.returnPressed.connect(self.input_processing)

        self.input_layout = QtWidgets.QHBoxLayout()
        self.input_layout.addWidget(self.input_cmd)

        layout.addWidget(self.output)
        layout.addLayout(self.input_layout)

        self.bootup_message()

    def bootup_message(self):
        date = str(time.localtime().tm_mday) + "/" + str(time.localtime().tm_mon) + "/" + str(time.localtime().tm_year)
        time_current = str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + "." + str(time.localtime().tm_sec)
        self.output.append("|-- <b>FILOSH v1.0</b> --|")
        self.output.append(f"session started on {date} at {time_current}<br>")
        self.output.append("!! Type <b>help</b> for a list of commands !!")
        self.output.append("----------------------------------------------<br>")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setBrush(QtGui.QColor("#0F0F0F"))
        painter.setPen(QtCore.Qt.PenStyle.NoPen)

        if self.is_maximized:
            painter.drawRect(QtCore.QRectF(0, 0, self.width(), self.height()))
        else:
            painter.drawRoundedRect(QtCore.QRectF(0, 0, self.width(), self.height()), 10, 10)

    def input_processing(self):
        line = 1 #- implementing later on
        user_in = self.input_cmd.text()

        if len(user_in) > 0:
            parsed = self.parser.parse(user_in)
            self.output.append(f"{os.getcwd()}$: {parsed}")
            self.input_cmd.clear()
            line += 1