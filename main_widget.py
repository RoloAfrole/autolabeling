# -*- coding: utf-8 -*-

import sys
import os

import cv2

import json

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QTimer, QSize
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QPushButton
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide2.QtUiTools import QUiLoader

from capture_settings import CaptureSettingWidget
from camera_frame import CameraFrame

from autolabeling_utils import (
    detail_now_name,
    create_circle_labelme_json,
    convert_valid_json_data,
)


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.video_size = QSize(800, 600)
        self.set_init_settings()
        self.setup_ui()
        self.setup_camera()

    def set_init_settings(self):
        self.record_mode = False
        self.record_timer = None
        self.frame_count = 0

    def setup_ui(self):
        """Initialize widgets.
        """
        self.image_label = CameraFrame()
        self.image_label.setFixedSize(self.video_size)

        self.record_button = QPushButton("Record")
        self.stop_button = QPushButton("Stop")
        self.record_button.clicked.connect(self.start_record)
        self.stop_button.clicked.connect(self.stop_record)

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

        self.record_timer = QTimer()
        self.record_timer.timeout.connect(self.save_data)
        self.change_record_mode(self.record_mode)

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
        pos, r = self.get_pos_r()
        frame = cv2.circle(
            frame, pos, r, (255, 69, 0), thickness=1, lineType=cv2.LINE_AA, shift=0,
        )
        frame = cv2.circle(
            frame, pos, 1, (255, 69, 0), thickness=-1, lineType=cv2.LINE_AA, shift=0,
        )
        return frame

    def get_pos_r(self):
        if self.capture_setting.use_cursor:
            if self.image_label.npos is not None:
                return (
                    (self.image_label.npos.x(), self.image_label.npos.y()),
                    int(self.capture_setting.RADIUS * self.image_label.r_amp),
                )
            else:
                return (0, 0), self.capture_setting.RADIUS
        else:
            return (
                (self.capture_setting.X, self.capture_setting.Y),
                self.capture_setting.RADIUS,
            )

    def start_record(self):
        self.frame_count = 0
        self.record_mode = True
        self.change_record_mode(self.record_mode)
        self.capture_setting.set_save_dirpath()
        self.start_record_timer()

    def stop_record(self):
        self.stop_record_timer()
        convert_valid_json_data(self.capture_setting.get_full_save_dirpath())
        self.record_mode = False
        self.change_record_mode(self.record_mode)

    def start_record_timer(self):
        self.record_timer.start(int(1000 / self.capture_setting.captur_frame_per_s))

    def stop_record_timer(self):
        self.record_timer.stop()

    def save_data(self):
        self.frame_count += 1
        _, frame = self.capture.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        pos, r = self.get_pos_r()

        # base_name = detail_now_name()
        base_name = "{:04}_{:02}".format(
            int(self.frame_count / self.capture_setting.captur_frame_per_s),
            self.frame_count % self.capture_setting.captur_frame_per_s,
        )
        dirpath = self.capture_setting.get_full_save_dirpath()
        image_name = "{}.png".format(base_name)

        self.write_image(frame, os.path.join(dirpath, image_name))

        json_data = create_circle_labelme_json(
            pos, r, image_name, self.video_size.height(), self.video_size.width(), frame
        )
        json_path = "{}.json".format(base_name)
        with open(os.path.join(dirpath, json_path), "w") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

    def write_image(self, frame, image_path):
        cv2.imwrite(image_path, frame)

    def change_record_mode(self, new_mode):
        if new_mode:
            self.record_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.stop_button.setEnabled(False)
            self.record_button.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWidget()
    mainWindow.show()
    sys.exit(app.exec_())
