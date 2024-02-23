from PyQt5 import QtWidgets, uic

import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("mainwindow.ui", self)

        self.widget_rx.canvas.ax.plot([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 2, 1, 0, 3, 1, 0], "r")
        self.widget_rx.canvas.draw()

        self.widget_tx.canvas.ax.plot([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 2, 2, 3, 0, 0, 1, 1, 0], "g")
        self.widget_tx.canvas.draw()

        
        # self.widget_DV.canvas.draw()
