import sys
import pandas as pd
import sqlite3

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox,
    QTableWidgetItem)

from PyQt5.uic import loadUi

import MainMenu_ui
import MatchWindow_ui
import AddWindow_ui
import PredictionModel


class Main(QDialog, MainMenu_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.conn = sqlite3.connect('premier_league.db')
        self.PM = PredictionModel.PredictionModel()

        sql_query = pd.read_sql_query(
            "select * from Historical_matches", self.conn)
        df = pd.DataFrame(sql_query, columns=['season'])
        seasons = df.season.unique().tolist()

        seasons.append('2020/21')
        seasons.remove('1995/96')
        seasons.remove('1996/97')
        seasons.remove('1997/98')
        for x in seasons:
            self.SeasonComboBox.addItem(x)

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
        temp, temp2 = self.PM.predict_season(int(self.SeasonComboBox.currentText()[:-3]))
        if (self.viewButton.isChecked()):
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(temp.shape[0])
            self.tableWidget.setHorizontalHeaderLabels(["Gospodarz", "Gość", "Wynik"])

            for n, x in enumerate(temp.iterrows()):
                self.tableWidget.setItem(n, 0, QTableWidgetItem(x[1][0]))  # Nazwa Gospodarza
                self.tableWidget.setItem(n, 1, QTableWidgetItem(x[1][1]))  # Nazwa Gościa
                self.tableWidget.setItem(n, 2, QTableWidgetItem(x[1][2]))  # Ktora druzyna wygrala
        else:
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setRowCount(temp2.shape[0])
            self.tableWidget.setHorizontalHeaderLabels(
                ["Drużyna", "Wygrane", "Remisy", "Przegrane", "Punkty"])

            for n, x in enumerate(temp2.iterrows()):
                self.tableWidget.setItem(n, 0, QTableWidgetItem(x[1][0]))  # Nazwa Drużyny
                self.tableWidget.setItem(n, 1, QTableWidgetItem(str(int(x[1][2]))))  # Ilość wygranych meczy
                self.tableWidget.setItem(n, 2, QTableWidgetItem(str(int(x[1][4]))))  # Ilość zremisowanych meczy
                self.tableWidget.setItem(n, 3, QTableWidgetItem(str(int(x[1][3]))))  # Ilość przegranych meczy
                self.tableWidget.setItem(n, 4, QTableWidgetItem(str(int(x[1][1]))))  # Ilość zdobytych punktów


class Match(QDialog, MatchWindow_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        for x in range(10):
            self.ARedComboBox.addItem(str(x))
            self.AInjurComboBox.addItem(str(x))
            self.HRedComboBox.addItem(str(x))
            self.HInjurComboBox.addItem(str(x))
        teams = ["Liverpool", "Manchester City", "Manchester United", "Chelsea", "Leicester City",
                 "Tottenham Hotspur",
                 "Wolverhampton Wanderers", "Arsenal", "Sheffield United", "Burnley", "Southampton", "Everton",
                 "Newcastle United", "Crystal Palace", "Brighton & Hove Albion", "West Ham United",
                 "Aston Villa",
                 "Leeds United", "West Bromwich Albion", "Fulham"]
        teams.sort()

        for t in teams:
            self.HomeComboBox.addItem(t)
            self.AwayComboBox.addItem(t)

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
        self.conn = sqlite3.connect('premier_league.db')

        self.WinnerBox.addItem('Gość')
        self.WinnerBox.addItem('Gospodarz')
        self.WinnerBox.addItem('Remis')
        self.fill_teams()

    def connectSignalsSlots(self):
        self.AddButton.clicked.connect(self.addMatch)
        self.CancelButton.clicked.connect(self.Cancel)

    def fill_teams(self):
        teams = ["Liverpool", "Manchester City", "Manchester United", "Chelsea", "Leicester City",
                          "Tottenham Hotspur",
                          "Wolverhampton Wanderers", "Arsenal", "Sheffield United", "Burnley", "Southampton", "Everton",
                          "Newcastle United", "Crystal Palace", "Brighton & Hove Albion", "West Ham United",
                          "Aston Villa",
                          "Leeds United", "West Bromwich Albion", "Fulham"]
        teams.sort()
        for team in teams:
            self.HomeTeamBox.addItem(team)
            self.AwayTeamBox.addItem(team)

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
