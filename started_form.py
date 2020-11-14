import sqlite3
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore


class StartForm(QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        """Создаёт базовый класс для аутентификации и регистрации"""
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("database.sqlite")
        self.cur = self.con.cursor()
        self.pass_edit.setEchoMode(QLineEdit.Password)

    def closeEvent(self, event):
        self.con.commit()
        self.con.close()
