# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vid.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import cv2
import numpy as np
import time
import PoseModule as pm
from PyQt5 import QtCore, QtGui, QtWidgets


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        location = f'Videos/{self.workout}/{self.file}'
        cap = cv2.VideoCapture(location)
        newlocation = 'Finished/' + self.workout + '_' + self.file
        result = cv2.VideoWriter(newlocation, cv2.VideoWriter_fourcc(*'MJPG'), 30, (1280, 720))

        detector = pm.poseDetector()
        count = 0
        """0 - going down, 1 - going up"""

        brown = (48, 0, 73)
        blue = (214, 50, 40)
        orange = (247, 127, 0)
        lightBlue = (252, 181, 73)
        white = (255, 255, 255)
        red = (0, 0, 255)
        barColor = blue

        start = time.time()
        direction = 0

        leftTopCorrection = ""
        leftDownCorrection = ""
        rightTopCorrection = ""
        rightDownCorrection = ""

        shoulderTopCorrection = ""
        shoulderDownCorrection = ""
        hipRightTopCorrection = ""
        hipLeftTopCorrection = ""
        elbowRightTopCorrection = ""
        elbowLeftTopCorrection = ""
        spineCorrection = ""
        legCorrection = ""

        hipLeftBottomAngle = []
        minHipLeftAngle = {}
        hipLeftTopAngle = []
        maxHipLeftAngle = {}

        hipRightBottomAngle = []
        minHipRightAngle = {}
        hipRightTopAngle = []
        maxHipRightAngle = {}

        bottomLegLeftAngle = []
        minBottomLegLeftAngle = {}
        topLegLeftAngle = []
        maxTopLegLeftAngle = {}

        bottomLegRightAngle = []
        minBottomLegRightAngle = {}
        topLegRightAngle = []
        maxTopLegRightAngle = {}

        bottomShoulderLeftAngle = []
        minBottomShoulderLeftAngle = {}
        topShoulderLeftAngle = []
        maxTopShoulderLeftAngle = {}

        bottomShoulderRightAngle = []
        minBottomShoulderRightAngle = {}
        topShoulderRightAngle = []
        maxTopShoulderRightAngle = {}

        bottomElbowLeftAngle = []
        minBottomElbowLeftAngle = {}
        topElbowLeftAngle = []
        maxTopElbowLeftAngle = {}

        bottomElbowRightAngle = []
        minBottomElbowRightAngle = {}
        topElbowRightAngle = []
        maxTopElbowRightAngle = {}

        elbowLeftDownAngle = []
        minElbowLeftDownAngle = {}
        elbowLeftUpAngle = []
        maxElbowLeftUpAngle = {}

        elbowRightDownAngle = []
        minElbowRightDownAngle = {}
        elbowRightUpAngle = []
        maxElbowRightUpAngle = {}

        startPosition = False
        while True:
            try:
                success, img = cap.read()
                # img = cv2.flip(img, 1)
                img = cv2.resize(img, (1280, 720))
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)
                if len(lmList) != 0:
                    """The basis for correctness and counting of push ups"""
                    elbowRightAngle = detector.findAngle(img, 12, 14, 16)
                    elbowLeftAngle = detector.findAngle(img, 11, 13, 15)
                    legLeftAngle = detector.findAngle(img, 23, 25, 27)
                    legRightAngle = detector.findAngle(img, 24, 26, 28)
                    hipLeftAngle = detector.findAngle(img, 11, 23, 25)
                    hipRightAngle = detector.findAngle(img, 12, 24, 26)
                    shoulderRightAngle = detector.findAngle(img, 14, 12, 24)
                    shoulderLeftAngle = detector.findAngle(img, 13, 11, 23)

                    perLeftHips = np.interp(hipLeftAngle, (155, 170), (100, 0))
                    perRightHips = np.interp(hipRightAngle, (155, 170), (100, 0))
                    # perLeftElbow = np.interp(elbowLeftAngle, (145, 170), (0, 100))
                    # perRightElbow = np.interp(elbowRightAngle, (145, 170), (0, 100))
                    # bar = np.interp(legLeftAngle, (90, 160), (650, 100))

                    # if int(spineAngle) in range(170, 190) and int(legLeftAngle) > 150:
                    startPosition = True
                    if startPosition:
                        if perLeftHips == 0 and perRightHips == 0:
                            barColor = lightBlue
                            if direction == 0:
                                count += 0.5
                                direction = 1
                                print("0")
                        if perLeftHips == 100 and perRightHips == 100:
                            barColor = lightBlue
                            if direction == 1:
                                count += 0.5
                                direction = 0
                                print("1")

                        if int(count) > 0:

                            if legLeftAngle < 160 or legRightAngle:
                                legCorrection = "straighten your legs"

                            if direction == 0:
                                hipLeftTopAngle.append(round(hipLeftAngle))
                                maxHipLeftAngle[count] = []
                                maxHipLeftAngle[count] += hipLeftTopAngle

                                elbowLeftUpAngle.append(round(elbowLeftAngle))
                                maxElbowLeftUpAngle[count] = []
                                maxElbowLeftUpAngle[count] += elbowLeftUpAngle

                                hipRightTopAngle.append(round(hipRightAngle))
                                maxHipRightAngle[count] = []
                                maxHipRightAngle[count] += hipRightTopAngle

                                elbowRightUpAngle.append(round(elbowRightAngle))
                                maxElbowRightUpAngle[count] = []
                                maxElbowRightUpAngle[count] += elbowRightUpAngle

                                for key, value in maxTopElbowLeftAngle.items():
                                    if max(value) < 150:
                                        elbowLeftTopCorrection = "rest your elbows"

                                for key, value in maxTopElbowRightAngle.items():
                                    if max(value) < 150:
                                        elbowRightTopCorrection = "rest your elbows"
                                for key, value in maxHipLeftAngle.items():
                                    if max(value) < 150:
                                        hipLeftTopCorrection = "straight your legs"

                                for key, value in maxHipRightAngle.items():
                                    if max(value) < 150:
                                        hipRightTopCorrection = "straight your legs"

                            """ERRORS direction = 1 | going up"""
                            if direction == 1:  # going up
                                hipRightBottomAngle.append(round(hipRightAngle))
                                minHipRightAngle[count] = []
                                minHipRightAngle[count] += hipRightBottomAngle

                                bottomElbowRightAngle.append(round(elbowRightAngle));
                                minBottomElbowRightAngle[count] = []
                                minBottomElbowRightAngle[count] += bottomElbowRightAngle

                                hipLeftBottomAngle.append(round(hipLeftAngle))
                                minHipLeftAngle[count] = []
                                minHipLeftAngle[count] += hipLeftBottomAngle

                                bottomElbowLeftAngle.append(round(elbowLeftAngle));
                                minBottomElbowLeftAngle[count] = []
                                minBottomElbowLeftAngle[count] += bottomElbowLeftAngle

                            for key, value in minBottomElbowLeftAngle.items():
                                if min(value) < 130:
                                    elbowLeftTopCorrection = "reach your elbows up high"

                            for key, value in minBottomElbowRightAngle.items():
                                if min(value) < 130:
                                    elbowRightTopCorrection = "extend your right elbow more"
                            for key, value in minHipLeftAngle.items():
                                if min(value) > 90:
                                    hipLeftTopCorrection = "open more"

                            for key, value in minHipRightAngle.items():
                                if min(value) > 150:
                                    hipRightTopCorrection = "open more"

                    corrections = [
                        hipRightTopCorrection,
                        hipLeftTopCorrection,
                        elbowRightTopCorrection,
                        elbowLeftTopCorrection,
                        legCorrection
                    ]
                    for x, correction in enumerate(corrections):
                        cv2.putText(img, correction, (10, (int(x) * 50) + 150), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

                    cv2.rectangle(img, (5, 5), (150, 100), lightBlue, cv2.FILLED)
                    cv2.putText(img, str(int(count)), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                blue, 10)

                end = time.time()
                duration = end - start
                cv2.putText(img, f"Time: {round(duration, 1)} secs", (170, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            brown, 2)

                result.write(img)
                if success:
                    self.change_pixmap_signal.emit(img)
            except:
                # print("error")
                cap.release()
                cv2.destroyAllWindows()


class JumpingJacks(object):
    def __init__(self, workout, file):
        self.workout = workout
        self.file = file

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 980)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(6, 2, 1280, 720))
        self.image_label.setObjectName("image_label")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 740, 711, 16))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowTitle(self.workout)
        self.display_width = 1280
        self.display_height = 720
        # self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        self.thread = VideoThread()
        self.thread.workout = self.workout
        self.thread.file = self.file
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def update_image(self, img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = JumpingJacks("bicyclecrunch", "1.mp4")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    print(ui.newlocation)
