from mainwindow import MainWindow
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    main = MainWindow()
    main.show()

    app.exec_()