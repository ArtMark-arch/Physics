# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_authorization.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class AuthorizationForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title_label = QtWidgets.QLabel(Form)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.verticalLayout.addWidget(self.title_label)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.login_label = QtWidgets.QLabel(Form)
        self.login_label.setObjectName("login_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.login_label)
        self.pass_label = QtWidgets.QLabel(Form)
        self.pass_label.setObjectName("pass_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pass_label)
        self.login_edit = QtWidgets.QLineEdit(Form)
        self.login_edit.setObjectName("login_edit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.login_edit)
        self.pass_edit = QtWidgets.QLineEdit(Form)
        self.pass_edit.setObjectName("pass_edit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pass_edit)
        self.verticalLayout.addLayout(self.formLayout)
        self.login_button = QtWidgets.QPushButton(Form)
        self.login_button.setObjectName("login_button")
        self.verticalLayout.addWidget(self.login_button)
        self.registration_button = QtWidgets.QPushButton(Form)
        self.registration_button.setObjectName("registration_button")
        self.verticalLayout.addWidget(self.registration_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Авторизация"))
        self.title_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; font-style:italic;\">Авторизация</span></p></body></html>"))
        self.login_label.setText(_translate("Form", "логин"))
        self.pass_label.setText(_translate("Form", "пароль"))
        self.login_button.setText(_translate("Form", "войти"))
        self.registration_button.setText(_translate("Form", "регистрация"))