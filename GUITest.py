import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox,
    QTableWidgetItem)
from PyQt5.uic import loadUi

from MainMenu_ui import Ui_Dialog

class Window(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #self.connectSignalsSlots()
        self.SeasonComboBox.addItem("2020/2021")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(20)
        for x in range(20):
            self.tableWidget.setItem(x, 0, QTableWidgetItem("Home"))
            self.tableWidget.setItem(x, 1, QTableWidgetItem("Away"))
            self.tableWidget.setItem(x, 2, QTableWidgetItem("Winner"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())