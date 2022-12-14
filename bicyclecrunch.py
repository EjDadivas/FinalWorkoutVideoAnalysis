# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vid.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import math
import time
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QPixmap

import PoseModule as pm


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        location = f'Videos/{self.workout}/{self.file}.mp4'
        cap = cv2.VideoCapture(location)
        # newlocation = 'Finished/' + self.workout +'_'+ self.file
        # result = cv2.VideoWriter(newlocation, cv2.VideoWriter_fourcc(*'MJPG'), 30, (1280, 720))

        detector = pm.poseDetector()
        count = 0
        """0 - going down, 1 - going up"""
        direction = 0
        start = time.time()
        brown = (48, 0, 73)
        blue = (214, 50, 40)
        orange = (247, 127, 0)
        lightBlue = (252, 181, 73)
        white = (255, 255, 255)
        red = (0, 0, 255)
        barColor = blue

        text = []
        corrections = []

        leftTopCorrection = ""
        leftDownCorrection = ""
        rightTopCorrection = ""
        rightDownCorrection = ""
        elbowCorrection = ""
        shoulderTopCorrection = ""
        shoulderDownCorrection = ""
        spineCorrection = ""

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

        startPosition = False
        while True:
            try:
                success, img = cap.read()
                # img = cv2.flip(img, 1)
                img = cv2.resize(img, (1280, 720))
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)
                if len(lmList) != 0:
                    spineAngle = detector.findAngle(img, 7, 11, 23)
                    shoulderRightAngle = detector.findAngle(img, 14, 12, 24, False)
                    shoulderLeftAngle = detector.findAngle(img, 13, 11, 23, False)

                    elbowRightAngle = detector.findAngle(img, 12, 14, 16, False)
                    elbowLeftAngle = detector.findAngle(img, 11, 13, 15)

                    legRightAngle = detector.findAngle(img, 24, 26, 28)
                    legLeftAngle = detector.findAngle(img, 23, 25, 27)

                    hipRightAngle = detector.findAngle(img, 12, 24, 26, False)
                    hipLeftAngle = detector.findAngle(img, 11, 23, 25)

                    perLeft = np.interp(legLeftAngle, (60, 150), (0, 100))
                    perRight = np.interp(legRightAngle, (60, 150), (0, 100))

                    perShoulder = np.interp(shoulderLeftAngle, (90, 150), (0, 100))

                    if int(spineAngle) in range(80, 180):
                    # startPosition = True
                    # if startPosition:
                        if perLeft == 0 and perShoulder == 100:
                            barColor = lightBlue
                            if direction == 0:
                                count += 1
                                direction = 1

                        if perRight == 0 and perShoulder == 0:
                            barColor = lightBlue
                            if direction == 1:
                                count += 1
                                direction = 0

                        if int(count) > 0:
                            # if int(spineAngle) not in range(150, 190):
                            #     spineCorrection = "Straighten your back and look in front"
                            # if int(shoulderLeftAngle) not in range(60, 90):
                            #     shoulderCorrection = "Straighten back and shoulders."
                            # if int(elbowLeftAngle) not in range(150, 190):
                            #     elbowCorrection = "Straighen your arms "

                            if direction == 1:
                                # min left leg
                                bottomLegLeftAngle.append(round(legLeftAngle));
                                minBottomLegLeftAngle[count] = []
                                minBottomLegLeftAngle[count] += bottomLegLeftAngle

                                # max right leg
                                topLegRightAngle.append(round(legRightAngle))
                                maxTopLegRightAngle[count] = []
                                maxTopLegRightAngle[count] += topLegRightAngle

                                topShoulderLeftAngle.append(round(shoulderLeftAngle))
                                maxTopShoulderLeftAngle[count] = []
                                maxTopShoulderLeftAngle[count] += topShoulderLeftAngle

                                for key, value in minBottomLegLeftAngle.items():
                                    if min(value) > 90:
                                        leftDownCorrection = "bend your left leg"
                                        text.append(f"{leftDownCorrection} at {math.ceil(count)}")
                                        corrections.append(leftDownCorrection)
                                for key, value in maxTopLegRightAngle.items():
                                    print(max(value))
                                    if max(value) < 150:
                                        rightTopCorrection = "Extend your Right leg more"
                                        text.append(f"{rightTopCorrection} at {math.ceil(count)}")
                                        corrections.append(rightTopCorrection)

                                for key, value in maxTopShoulderLeftAngle.items():
                                    if max(value) < 150:
                                        shoulderTopCorrection = "extend your Left shoulder more"
                                        text.append(f"{shoulderTopCorrection} at {math.ceil(count)}")
                                        corrections.append(shoulderTopCorrection)

                            if direction == 0:  # going up
                                topLegLeftAngle.append(round(legLeftAngle))
                                maxTopLegLeftAngle[count] = []
                                maxTopLegLeftAngle[count] += topLegLeftAngle

                                bottomLegRightAngle.append(round(legRightAngle))
                                minBottomLegRightAngle[count] = []
                                minBottomLegRightAngle[count] += bottomLegRightAngle

                                bottomShoulderLeftAngle.append(round(shoulderLeftAngle))
                                minBottomShoulderLeftAngle[count] = []
                                minBottomShoulderLeftAngle[count] += bottomShoulderLeftAngle

                                for key, value in maxTopLegLeftAngle.items():
                                    if max(value) < 150:
                                        leftTopCorrection = "extend your left leg more"
                                        text.append(f"{leftTopCorrection} at {math.ceil(count)}")
                                        corrections.append(leftTopCorrection)

                                for key, value in minBottomLegRightAngle.items():
                                    if min(value) > 90:
                                        rightDownCorrection = "bend your right leg more"
                                        text.append(f"{rightDownCorrection} at {math.ceil(count)}")
                                        corrections.append(rightDownCorrection)

                                for key, value in minBottomShoulderLeftAngle.items():
                                    if min(value) > 90:
                                        shoulderDownCorrection = "bend your right shoulder more"
                                        text.append(f"{shoulderDownCorrection} at {math.ceil(count)}")
                                        corrections.append(shoulderDownCorrection)

                        # corrections = [shoulderTopCorrection, shoulderDownCorrection, rightTopCorrection,
                        #                rightDownCorrection,
                        #                leftTopCorrection, leftDownCorrection, spineCorrection, elbowCorrection]
                        corrections = list(dict.fromkeys(corrections))
                        for x, correction in enumerate(corrections):
                            cv2.putText(img, correction, (10, (int(x) * 50) + 150), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

                        cv2.rectangle(img, (5, 5), (150, 100), lightBlue, cv2.FILLED)
                        cv2.putText(img, str(int(count)), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 3,
                                    blue, 10)
                        cv2.imwrite(f"Finished/{self.workout}_{self.file}.jpg", img)
                end = time.time()
                duration = end - start
                cv2.putText(img, f"Time: {round(duration, 1)} secs", (170, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            brown, 2)

                # result.write(img)
                if success:
                    self.change_pixmap_signal.emit(img)
                    print(corrections)
                    text.sort()
                    text = list(dict.fromkeys(text))
                    print(text)
                    with open(f"Finished/{self.workout}_{self.file}.txt", "w") as textfile:
                        textfile.write(f"Total count: {math.ceil(count)}\n")
                        for items in text:
                            textfile.write(f"{items}\n")
            except:
                # print("error")
                cap.release()
                cv2.destroyAllWindows()


class BicycleCrunch(object):
    def __init__(self, workout, file):
        self.workout = workout
        self.file = file

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
    ui = BicycleCrunch("bicyclecrunch", "2")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    print(ui.newlocation)
