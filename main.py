# -*- coding: utf-8 -*-

import sys
import os


from PySide2 import QtWidgets
from main_widget import MainWidget
from absl import app


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)


def main(argv):
    qapp = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(qapp.exec_())


if __name__ == "__main__":
    app.run(main)
