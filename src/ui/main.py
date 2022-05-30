# Filename: main_window.py

"""Main Window-Style application."""

import sys

from PyQt5.QtWidgets import QApplication, QTableWidget, QGridLayout, QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QTableWidgetItem

from src.db.database import  DatabaseManager

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.database = DatabaseManager()


        self.initUI()

    def initUI(self):
        decks = self.database.retrieve("SELECT * FROM DECKS;")
        for x in range(0, len(decks)):
            widget = QLabel(decks[x][0],self)
            widget.move(10, 10+1*x)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('QMainWindow')
        self.setCentralWidget(Example())
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self.gridLayout = QGridLayout()

        self.database = DatabaseManager()


    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        #status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


    def createTable(self):
        # Create table
        decks = self.database.retrieve("SELECT * FROM DECKS;")
        print(decks)
        count = self.database.retrieve("SELECT COUNT(*) FROM DECKS")[0]
        print(count)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(count[0])
        self.tableWidget.setColumnCount(2)
        for x in range(0,len(decks)):

            self.tableWidget.setItem(x, 0, QTableWidgetItem( decks[x][0] ))
            self.tableWidget.setItem(x, 1, QTableWidgetItem( decks[x][1] ))


        self.tableWidget.move(0, 0)
        self.setCentralWidget(self.tableWidget)

        # table selection change
        #self.tableWidget.doubleClicked.connect(self.on_click)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
