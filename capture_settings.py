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


class CaptureSettingWidget(QWidget):
    def __init__(self, parent=None):
        super(CaptureSettingWidget, self).__init__(parent)
        self.setup_settings()
        self.setup_ui()

    def setup_settings(self):
        """Initialize widgets params.
        """
        pass

    def setup_ui(self):
        """Initialize widgets.
        """
        self.RADIUS = 50
        self.X = 100
        self.Y = 100
        # self.use_cursor = False
        self.use_cursor = True

        self.setting_label = QLabel('Radius: {} px, X, Y = {}, {}'.format(self.RADIUS, self.X, self.Y))
        
        self.radius_label = QLabel('Radius:')
        self.radius_line_edit = QLineEdit('{}'.format(self.RADIUS))
        self.radius_unit_label = QLabel('px')

        self.radius_layout = QHBoxLayout()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_line_edit)
        self.radius_layout.addWidget(self.radius_unit_label)

        self.x_label = QLabel('X:')
        self.x_line_edit = QLineEdit('{}'.format(self.X))
        self.xy_sep_label = QLabel(', ')
        self.y_label = QLabel('Y:')
        self.y_line_edit = QLineEdit('{}'.format(self.Y))

        self.xy_layout = QHBoxLayout()
        self.xy_layout.addWidget(self.x_label)
        self.xy_layout.addWidget(self.x_line_edit)
        self.xy_layout.addWidget(self.xy_sep_label)
        self.xy_layout.addWidget(self.y_label)
        self.xy_layout.addWidget(self.y_line_edit)

        self.set_button = QPushButton("Set")
        self.set_button.clicked.connect(self.set_settings)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.setting_label)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.xy_layout)
        self.main_layout.addWidget(self.set_button)

        self.setLayout(self.main_layout)

    def set_settings(self):
        self.RADIUS = int(float(self.radius_line_edit.text()))
        self.X = int(float(self.x_line_edit.text()))
        self.Y = int(float(self.y_line_edit.text()))
        self.set_display_settings()
        self.set_edit_settings()

    def set_settings_by_input(self, radius, x, y):
        self.RADIUS = int(float(radius))
        self.X = int(float(x))
        self.Y = int(float(y))
        self.set_display_settings()
        self.set_edit_settings()

    def set_display_settings(self):
        self.setting_label.setText('Radius: {} px, X, Y = {}, {}'.format(self.RADIUS, self.X, self.Y))

    def set_edit_settings(self):
        self.radius_line_edit.setText('{}'.format(self.RADIUS))
        self.x_line_edit.setText('{}'.format(self.X))
        self.y_line_edit.setText('{}'.format(self.Y))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CaptureSettingWidget()
    mainWindow.show()
    sys.exit(app.exec_())
