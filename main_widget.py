# -*- coding: utf-8 -*-

import sys
import os

import cv2

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide2.QtUiTools import QUiLoader

from capture_settings import CaptureSettingWidget


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.video_size = QSize(800, 600)
        self.setup_ui()
        self.setup_camera()

    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = QLabel()
        self.image_label.setFixedSize(self.video_size)

        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        # self.record_button.clicked.connect(self.close)

        self.capture_setting = CaptureSettingWidget()

        self.sub1_layout = QVBoxLayout()
        self.sub1_layout.addWidget(self.image_label)
        self.sub12_layout = QHBoxLayout()
        self.sub12_layout.addWidget(self.record_button)
        self.sub12_layout.addWidget(self.stop_button)
        self.sub1_layout.addLayout(self.sub12_layout)

        self.sub2_layout = QVBoxLayout()
        self.sub2_layout.addWidget(self.capture_setting)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.sub1_layout)
        self.main_layout.addLayout(self.sub2_layout)

        self.setLayout(self.main_layout)

    def setup_camera(self):
        """Initialize camera.
        """
        self.capture = cv2.VideoCapture(1)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_size.width())
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_size.height())

        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        frame = self.draw_captured(frame)
        image = QImage(
            frame,
            frame.shape[1],
            frame.shape[0],
            frame.strides[0],
            QImage.Format_RGB888,
        )
        self.image_label.setPixmap(QPixmap.fromImage(image))

    def draw_captured(self, frame):
        frame = cv2.circle(
            frame,
            (self.capture_setting.X, self.capture_setting.Y),
            self.capture_setting.RADIUS,
            (255, 69, 0),
            thickness=1,
            lineType=cv2.LINE_AA,
            shift=0,
        )
        frame = cv2.circle(
            frame,
            (self.capture_setting.X, self.capture_setting.Y),
            1,
            (255, 69, 0),
            thickness=-1,
            lineType=cv2.LINE_AA,
            shift=0,
        )
        return frame

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWidget()
    mainWindow.show()
    sys.exit(app.exec_())
