# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("")
        Dialog.resize(775, 500)
        Dialog.setAccessibleName("")
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 441, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.SeasonComboBox = QtWidgets.QComboBox(Dialog)
        self.SeasonComboBox.setGeometry(QtCore.QRect(540, 150, 211, 22))
        self.SeasonComboBox.setAccessibleName("")
        self.SeasonComboBox.setObjectName("SeasonComboBox")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(480, 150, 56, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(460, 190, 311, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.SeasonButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.SeasonButton.setFont(font)
        self.SeasonButton.setObjectName("SeasonButton")
        self.verticalLayout.addWidget(self.SeasonButton)
        self.SaveButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.SaveButton.setFont(font)
        self.SaveButton.setObjectName("SaveButton")
        self.verticalLayout.addWidget(self.SaveButton)
        self.MatchButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.MatchButton.setFont(font)
        self.MatchButton.setObjectName("MatchButton")
        self.verticalLayout.addWidget(self.MatchButton)
        self.AddButton = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.AddButton.setFont(font)
        self.AddButton.setObjectName("AddButton")
        self.verticalLayout.addWidget(self.AddButton)
        self.viewButton = QtWidgets.QRadioButton(Dialog)
        self.viewButton.setGeometry(QtCore.QRect(480, 110, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.viewButton.setFont(font)
        self.viewButton.setObjectName("viewButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "System predykcji Premier League"))
        self.label_3.setText(_translate("Dialog", "Sezon:"))
        self.SeasonButton.setText(_translate("Dialog", "Symulacja wyników sezonu"))
        self.SaveButton.setText(_translate("Dialog", "Zapisz do bazy danych"))
        self.MatchButton.setText(_translate("Dialog", "Symulacja wyników meczu"))
        self.AddButton.setText(_translate("Dialog", "Dodaj wynik meczu"))
        self.viewButton.setText(_translate("Dialog", "Wyświetl wynik jako lista meczy"))
