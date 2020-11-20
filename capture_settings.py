# -*- coding: utf-8 -*-

import sys
import os

import cv2

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QCheckBox
from PySide2.QtUiTools import QUiLoader

from autolabeling_utils import checkdir

class CaptureSettingWidget(QWidget):
    def __init__(self, parent=None):
        super(CaptureSettingWidget, self).__init__(parent)
        self.setup_settings()
        self.setup_ui()

    def setup_settings(self):
        """Initialize widgets params.
        """
        self.RADIUS = 50
        self.X = 0
        self.Y = 0
        self.use_cursor = True
        self.captur_frame_per_s = 1
        self.root_save_dir = './captured'
        self.save_dir = None
        
        checkdir(self.root_save_dir, create=True)

    def setup_ui(self):
        """Initialize widgets.
        """
        self.setting_label = QLabel(self.get_display_str())

        self.radius_label = QLabel("Base Radius:")
        self.radius_line_edit = QLineEdit("{}".format(self.RADIUS))
        self.radius_unit_label = QLabel("px")

        self.radius_layout = QHBoxLayout()
        self.radius_layout.addWidget(self.radius_label)
        self.radius_layout.addWidget(self.radius_line_edit)
        self.radius_layout.addWidget(self.radius_unit_label)

        self.x_label = QLabel("X:")
        self.x_line_edit = QLineEdit("{}".format(self.X))
        self.xy_sep_label = QLabel(", ")
        self.y_label = QLabel("Y:")
        self.y_line_edit = QLineEdit("{}".format(self.Y))

        self.xy_layout = QHBoxLayout()
        self.xy_layout.addWidget(self.x_label)
        self.xy_layout.addWidget(self.x_line_edit)
        self.xy_layout.addWidget(self.xy_sep_label)
        self.xy_layout.addWidget(self.y_label)
        self.xy_layout.addWidget(self.y_line_edit)

        self.cursor_mode = QCheckBox("Cursor Mode")
        if self.use_cursor:
            self.cursor_mode.setChecked(self.use_cursor)

        self.capture_fps_label = QLabel("Capture fps:")
        self.capture_fps_line_edit = QLineEdit("{}".format(self.captur_frame_per_s))
        self.capture_fps_layout = QHBoxLayout()
        self.capture_fps_layout.addWidget(self.capture_fps_label)
        self.capture_fps_layout.addWidget(self.capture_fps_line_edit)

        self.set_button = QPushButton("Set")
        self.set_button.clicked.connect(self.set_settings)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.setting_label)
        self.main_layout.addLayout(self.radius_layout)
        self.main_layout.addLayout(self.xy_layout)
        self.main_layout.addWidget(self.cursor_mode)
        self.main_layout.addLayout(self.capture_fps_layout)
        self.main_layout.addWidget(self.set_button)

        self.setLayout(self.main_layout)

    def set_settings(self):
        self.set_settings_by_input(
            self.radius_line_edit.text(),
            self.x_line_edit.text(),
            self.y_line_edit.text(),
            self.cursor_mode.isChecked(),
            self.capture_fps_line_edit.text()
        )

    def set_settings_by_input(self, radius, x, y, is_checked, capture_fps):
        self.RADIUS = int(float(radius))
        self.X = int(float(x))
        self.Y = int(float(y))
        self.set_checkitems(is_checked)
        self.set_captur_frame_per_s(int(float(capture_fps)))
        self.set_display_settings()
        self.set_edit_settings()

    def set_display_settings(self):
        self.setting_label.setText(self.get_display_str())

    def get_display_str(self):
        return "Base Radius: {} px, X, Y = {}, {}\nCursor Mode: {}\nCapture fps: {}\nSave Dir: {}".format(
            self.RADIUS, self.X, self.Y, "On" if self.use_cursor else "Off", self.captur_frame_per_s, self.get_full_save_dirpath()
        )

    def set_edit_settings(self):
        self.radius_line_edit.setText("{}".format(self.RADIUS))
        self.x_line_edit.setText("{}".format(self.X))
        self.y_line_edit.setText("{}".format(self.Y))
        self.capture_fps_line_edit.setText("{}".format(self.captur_frame_per_s))

    def set_checkitems(self, is_checked):
        self.use_cursor = is_checked
        self.cursor_mode.setChecked(self.use_cursor)

    def set_captur_frame_per_s(self, new_num):
        if new_num <= 0:
            new_num = 1
        self.captur_frame_per_s = new_num

    def set_save_dirpath(self, dirname=None):
        if dirname is None:
            from autolabeling_utils import now_name
            dirname = now_name()
        self.save_dir = dirname
        checkdir(self.get_full_save_dirpath(), create=True)
        return dirname

    def get_full_save_dirpath(self):
        if self.save_dir is None:
            return self.root_save_dir
        else:
            return os.path.join(self.root_save_dir, self.save_dir)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = CaptureSettingWidget()
    mainWindow.show()
    sys.exit(app.exec_())
