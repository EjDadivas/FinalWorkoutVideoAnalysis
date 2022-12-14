# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vid.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import math
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import cv2
import numpy as np
import time
import PoseModule as pm
from PyQt5 import QtCore, QtGui, QtWidgets


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        location = self.filename
        print('old locaiton: ', location)
        cap = cv2.VideoCapture(location)


        newpath = os.path.split(location)
        newlocationFolder = f'Finished/{newpath[0]}'
        newlocationVid = f'Finished/{location}'
        print(newlocationFolder)
        if not os.path.exists(newlocationFolder):
            os.makedirs(newlocationFolder)
        print('newlocation for processd video:', newlocationFolder)
        result = cv2.VideoWriter(newlocationVid, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, (1280, 720))

        detector = pm.poseDetector()
        count = 0
        """0 - going down, 1 - going elbowUp"""
        direction = 0
        start = time.time()
        brown = (48, 0, 73)
        blue = (214, 50, 40)
        orange = (247, 127, 0)
        lighterblue = (252, 181, 73)
        white = (255, 255, 255)
        red = (0, 0, 255)
        barColor = blue
        text = []
        corrections = []

        elbowDownAngle = []
        minElbowDownAngle = {}
        elbowUpAngle = []
        maxElbowUpAngle = {}

        while True:
            try:
                success, img = cap.read()
                img = cv2.resize(img, (1280, 720))
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)

                if len(lmList) != 0:
                    rightLegAngle = detector.findAngle(img, 24, 26, 28, False)
                    elbowAngle = detector.findAngle(img, 11, 13, 15)
                    hipAngle = detector.findAngle(img, 11, 23, 25)
                    legAngle = detector.findAngle(img, 23, 25, 27)
                    handAngle = detector.findAngle(img, 13, 15, 19)
                    spineAngle = detector.findAngle(img, 7, 11, 23)
                    heelAngle = detector.findAngle(img, 25, 29, 31)

                    per = np.interp(elbowAngle, (130, 160), (0, 100))
                    bar = np.interp(elbowAngle, (90, 160), (650, 100))

                    if int(spineAngle) > 140 and int(heelAngle) in range(60, 90) and int(rightLegAngle) > 150 and int(
                            hipAngle) > 140 and int(handAngle) > 90:

                        if per == 0:
                            barColor = lighterblue
                            if direction == 0:
                                count += 0.5
                                direction = 1
                        if per == 100:
                            barColor = lighterblue
                            if direction == 1:
                                count += 0.5
                                direction = 0

                        if int(count) > 0:
                            if legAngle < 160:
                                legCorrection = "Legs are not straight"
                                text.append(f"{legCorrection} at {math.ceil(count)}")
                                corrections.append(legCorrection)

                            if hipAngle < 150:
                                hipCorrection = "Hips are not straight"
                                text.append(f"{hipCorrection} at {math.ceil(count)}")
                                corrections.append(hipCorrection)

                            if int(spineAngle) not in range(140, 180):
                                spineCorrection = "Keep your neck straight"
                                text.append(f"{spineCorrection} at {math.ceil(count)}")
                                corrections.append(spineCorrection)

                            """Errors | direction = 0/ going down angle"""
                            if direction == 0:
                                elbowUpAngle.append(round(elbowAngle))
                                maxElbowUpAngle[count] = []
                                maxElbowUpAngle[count] += elbowUpAngle

                            for key, value in maxElbowUpAngle.items():
                                # print(max(value))
                                if max(value) < 150:
                                    print(max(value))
                                    elbowUpCorrection = "Straighten your arms"
                                    text.append(f"{elbowUpCorrection} at {math.ceil(count)}")
                                    corrections.append(elbowUpCorrection)

                            """ERRORS direction = 1 | going elbowUp"""
                            if direction == 1:  # going elbowUp
                                elbowDownAngle.append(round(elbowAngle))
                                minElbowDownAngle[count] = []
                                minElbowDownAngle[count] += elbowDownAngle

                            for key, value in minElbowDownAngle.items():
                                if min(value) > 90:
                                    elbowDownCorrection = "you only did half push"
                                    text.append(f"{elbowDownCorrection} at {math.ceil(count)}")
                                    corrections.append(elbowDownCorrection)

                        corrections = list(dict.fromkeys(corrections))
                        for x, correction in enumerate(corrections):
                            cv2.putText(img, correction, (10, (int(x) * 50) + 150), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

                        cv2.rectangle(img, (1100, 100), (1175, 650), barColor, 1)
                        cv2.rectangle(img, (1100, int(bar)), (1175, 650), barColor, cv2.FILLED)
                        cv2.putText(img, f'{int(per)} %', (1100, 375), cv2.FONT_HERSHEY_PLAIN, 1.5,
                                    red, 2)

                        cv2.rectangle(img, (5, 5), (150, 100), lighterblue, cv2.FILLED)
                        cv2.putText(img, str(int(count)), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                    blue, 10)
                        # cv2.imwrite(f"Finished/{self.workout}_{self.file}.jpg", img)
                end = time.time()
                duration = end - start
                cv2.putText(img, f"Time: {round(duration, 1)} secs", (170, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            brown, 2)

                result.write(img)
                if success:
                    self.change_pixmap_signal.emit(img)
                    print(corrections)
                    text.sort()
                    text = list(dict.fromkeys(text))
                    print(text)
                    newlocationText = f"{newlocationFolder}/{self.file}.txt"
                    with open(newlocationText, "w") as textfile:
                        textfile.write(f"Total count: {math.ceil(count)}\n")
                        for items in text:
                            textfile.write(f"{items}\n")

            except:
                break
        cap.release()
        cv2.destroyAllWindows()


class Pushups(object):
    def __init__(self, filename, file):
        # self.workout = workout
        self.file = file
        self.filename = filename

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
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
        MainWindow.setWindowTitle("Push Ups")
        self.display_width = 1280
        self.display_height = 720
        # self.image_label = QLabel(self)
        self.image_label.resize(self.display_width, self.display_height)

        self.thread = VideoThread()
        # self.thread.workout = self.workout
        self.thread.file = self.file
        self.thread.filename = self.filename

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
    ui = Pushups("New/jm@gmail.com/1stWeek/PushUps/1.mp4", "1")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    print(ui.newlocation)
