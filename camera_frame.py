# -*- coding: utf-8 -*-

import sys
import os

import cv2

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide2.QtUiTools import QUiLoader


class CameraFrame(QLabel):
    def __init__(self, parent=None):
        super(CameraFrame, self).__init__(parent)
        self.npos = None
        self.r_amp = 1.0

    def mouseMoveEvent(self, event):
        self.npos = event.pos()

    def mousePressEvent(self, event):
        self.npos = event.pos()

    def wheelEvent(self, event):
        degress = event.angleDelta().y() / 8
        new_amp = self.r_amp + 0.3*degress/45
        if new_amp > 0.0:
            self.r_amp = new_amp
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CameraFrame()
    mainWindow.show()
    sys.exit(app.exec_())
