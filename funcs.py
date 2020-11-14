import os
import hashlib
import excepts
from PyQt5.QtWidgets import QMessageBox


def check_absence(login, password):
    """провека на пустые логин или пароль"""
    if login and password:
        return True
    raise excepts.AbsenceError


def show_message(message):
    """вывод сообщения об ошибке"""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("error")
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def hash_pass(password, salt=None, available_salt=None):
    """хеш пароля с уникальной солью."""
    if not salt:
        salt = os.urandom(32)
        if not available_salt:
            available_salt = []
        while any(filter(lambda sl: sl == salt, available_salt)):
            salt = os.urandom(32)
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000), salt
    else:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
