import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox,
    QTableWidgetItem)
from PyQt5.uic import loadUi

import MainMenu_ui
import MatchWindow_ui


class Main(QDialog, MainMenu_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.connectSignalsSlots()
        self.SeasonComboBox.addItem("2020/2021")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(20)
        for x in range(20):
            self.tableWidget.setItem(x, 0, QTableWidgetItem("Home"))
            self.tableWidget.setItem(x, 1, QTableWidgetItem("Away"))
            self.tableWidget.setItem(x, 2, QTableWidgetItem("Winner"))
        self.MatchButton.clicked.connect(self.on_MatchButton_clicked)
        self.dialog = Match(self)
    def on_MatchButton_clicked(self):
        self.dialog.exec()

class Match(QDialog, MatchWindow_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.backButton.clicked.connect(self.on_backButton_clicked)
    def on_backButton_clicked(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec())
