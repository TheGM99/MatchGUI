import sys

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox,
    QTableWidgetItem)

from PyQt5.uic import loadUi

import MainMenu_ui
import MatchWindow_ui
import AddWindow_ui


class Main(QDialog, MainMenu_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.SeasonComboBox.addItem("2020/2021")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(20)
        for x in range(20):
            self.tableWidget.setItem(x, 0, QTableWidgetItem("Home"))  # Nazwa Gospodarza
            self.tableWidget.setItem(x, 1, QTableWidgetItem("Away"))  # Nazwa Gościa
            self.tableWidget.setItem(x, 2, QTableWidgetItem("Winner"))  # Ktora druzyna wygrala

    def connectSignalsSlots(self):
        self.MatchButton.clicked.connect(self.openMatchWindow)
        self.AddButton.clicked.connect(self.openAddWindow)
        self.SaveButton.clicked.connect(self.saveToDB)
        self.SeasonButton.clicked.connect(self.generateSeason)

    def openMatchWindow(self):
        Match(self).exec()

    def openAddWindow(self):
        Add(self).exec()

    def saveToDB(self):
        # Tu zapisywanie wygenerowanych wyników do bd
        print()

    def generateSeason(self):
        # tu wygenerowanie wynikow sezonu
        print()


class Match(QDialog, MatchWindow_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        for x in range(10):
            self.ARedComboBox.addItem(str(x))
            self.AInjurComboBox.addItem(str(x))
            self.HRedComboBox.addItem(str(x))
            self.HInjurComboBox.addItem(str(x))

    def generateMatch(self):
        # tu generowanie pojedynczego meczu
        print()

    def saveMatch(self):
        # tu zapis pojedynczego meczu do DB
        print()

    def on_backButton_clicked(self):
        self.close()



class Add(QDialog, AddWindow_ui.Ui_AddWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.AddButton.clicked.connect(self.addMatch)
        self.CancelButton.clicked.connect(self.Cancel)

    def addMatch(self):
        # tu dodajemy mecz
        self.close()

    def Cancel(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Main()
    win.show()
    sys.exit(app.exec())
