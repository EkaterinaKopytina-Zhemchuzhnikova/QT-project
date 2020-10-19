# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_info_form.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(415, 627)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 0, 81, 16))
        self.label.setObjectName("label")
        self.calendar = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendar.setGeometry(QtCore.QRect(60, 30, 331, 201))
        self.calendar.setObjectName("calendar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 300, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 390, 111, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 460, 111, 16))
        self.label_4.setObjectName("label_4")
        self.patient_name = QtWidgets.QLineEdit(self.centralwidget)
        self.patient_name.setGeometry(QtCore.QRect(60, 420, 311, 20))
        self.patient_name.setObjectName("patient_name")
        self.patient_snils = QtWidgets.QLineEdit(self.centralwidget)
        self.patient_snils.setGeometry(QtCore.QRect(60, 490, 311, 20))
        self.patient_snils.setObjectName("patient_snils")
        self.btn_accept = QtWidgets.QPushButton(self.centralwidget)
        self.btn_accept.setGeometry(QtCore.QRect(140, 530, 141, 31))
        self.btn_accept.setObjectName("btn_accept")
        self.accept_message = QtWidgets.QLabel(self.centralwidget)
        self.accept_message.setGeometry(QtCore.QRect(120, 570, 191, 16))
        self.accept_message.setObjectName("accept_message")
        self.pbn_find = QtWidgets.QPushButton(self.centralwidget)
        self.pbn_find.setGeometry(QtCore.QRect(140, 240, 151, 23))
        self.pbn_find.setObjectName("pbn_find")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 415, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Выбор времени"))
        self.label.setText(_translate("MainWindow", "Выберите дату"))
        self.label_2.setText(_translate("MainWindow", "Выберите время"))
        self.label_3.setText(_translate("MainWindow", "Введите ваше ФИО"))
        self.label_4.setText(_translate("MainWindow", "Введите ваш СНИЛС"))
        self.btn_accept.setText(_translate("MainWindow", "Подтвердить запись"))
        self.accept_message.setText(_translate("MainWindow", "Ваша запись еще не подтверждена"))
        self.pbn_find.setText(_translate("MainWindow", "Найти свободное время"))
