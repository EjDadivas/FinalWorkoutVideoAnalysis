# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vid.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,  QMutex, QWaitCondition
import cv2
import numpy as np
import time
import PoseModule as pm
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow
import sys

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, mutex, condition):
        super().__init__()
        self.mutex = mutex
        self.condition = condition
    def run(self):
        location = f'Videos/{self.workout}/{self.file}'
        cap = cv2.VideoCapture(location)
        print(location)
        result = cv2.VideoWriter('Finished/' + self.workout + '_' + self.file,
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 30, (1280, 720))
        detector = pm.poseDetector()
        count = 0
        """0 - going down, 1 - going up"""
        directionR = 0
        directionL = 0
        start = time.time()
        brown = (48, 0, 73)
        blue = (214, 50, 40)
        orange = (247, 127, 0)
        lightBlue = (252, 181, 73)
        white = (255, 255, 255)
        red = (0, 0, 255)
        barColor = blue

        leftTopCorrection = ""
        leftDownCorrection = ""
        rightTopCorrection = ""
        rightDownCorrection = ""

        elbowCorrection = ""

        shoulderCorrection = ""
        spineCorrection = ""

        bottomLegLeftAngle = []
        minBottomLegLeftAngle = {}
        topLegLeftAngle = []
        maxTopLegLeftAngle = {}

        bottomLegRightAngle = []
        minBottomLegRightAngle = {}
        topLegRightAngle = []
        maxTopLegRightAngle = {}

        while True:
            try:
                success, img = cap.read()
                img = cv2.resize(img, (1280, 720))
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)
                if len(lmList) != 0:
                    """The basis for correctness and counting of push ups"""
                    elbowAngle = detector.findAngle(img, 11, 13, 15)
                    legLeftAngle = detector.findAngle(img, 23, 25, 27)
                    legRightAngle = detector.findAngle(img, 24, 26, 28)
                    """Checking the Form"""
                    spineAngle = detector.findAngle(img, 7, 11, 23, False)
                    shoulderAngle = detector.findAngle(img, 13, 11, 23)
                    hipAngle = detector.findAngle(img, 11, 23, 25)

                    perLeft = np.interp(legLeftAngle, (60, 150), (0, 100))
                    perRight = np.interp(legRightAngle, (60, 150), (0, 100))
                    # bar = np.interp(legLeftAngle, (90, 160), (650, 100))

                    # if int(spineAngle) in range(170, 190) and int(legLeftAngle) > 150:
                    startPosition = True
                    if startPosition:
                        if perLeft == 0:
                            barColor = lightBlue
                            if directionL == 0:
                                count += 0.5
                                directionL = 1
                        if perLeft == 100:
                            barColor = lightBlue
                            if directionL == 1:
                                count += 0.5
                                directionL = 0

                        if perRight == 0:
                            barColor = lightBlue
                            if directionR == 0:
                                count += 0.5
                                directionR = 1
                        if perRight == 100:
                            barColor = lightBlue
                            if directionR == 1:
                                count += 0.5
                                directionR = 0

                        if int(count) > 0:
                            if int(spineAngle) not in range(150, 190):
                                spineCorrection = "Straighten your back and look in front"
                            if int(shoulderAngle) not in range(60, 90):
                                shoulderCorrection = "Straighten back and shoulders."
                            if int(elbowAngle) not in range(150, 190):
                                elbowCorrection = "Straighen your arms "

                            if directionL == 0:
                                topLegLeftAngle.append(round(legLeftAngle));
                                maxTopLegLeftAngle[count] = []
                                maxTopLegLeftAngle[count] += topLegLeftAngle

                            """ERRORS direction = 1 | going up"""
                            if directionL == 1:  # going up
                                bottomLegLeftAngle.append(round(legLeftAngle));
                                minBottomLegLeftAngle[count] = []
                                minBottomLegLeftAngle[count] += bottomLegLeftAngle

                            for key, value in minBottomLegLeftAngle.items():
                                if min(value) > 90:
                                    leftDownCorrection = "left leg should be closeer to hand"

                            for key, value in maxTopLegLeftAngle.items():
                                if max(value) < 150:
                                    leftTopCorrection = f"extend your left leg more {count}"

                            if directionR == 0:
                                topLegRightAngle.append(round(legRightAngle));
                                maxTopLegRightAngle[count] = []
                                maxTopLegRightAngle[count] += topLegRightAngle

                            if directionR == 1:  # going up
                                bottomLegRightAngle.append(round(legRightAngle));
                                minBottomLegRightAngle[count] = []
                                minBottomLegRightAngle[count] += bottomLegRightAngle

                            for key, value in minBottomLegRightAngle.items():
                                if min(value) > 90:
                                    rightDownCorrection = "Right leg should be closeer to hand"

                            for key, value in maxTopLegRightAngle.items():
                                if max(value) < 150:
                                    rightTopCorrection = "extend your Right leg more"

                    cv2.putText(img, shoulderCorrection, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                    cv2.putText(img, rightDownCorrection, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                    cv2.putText(img, rightTopCorrection, (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                    cv2.putText(img, spineCorrection, (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                    cv2.putText(img, leftDownCorrection, (10, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                    cv2.putText(img, leftTopCorrection, (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
                    cv2.putText(img, elbowCorrection, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)

                    # Draw Count
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
                    self.condition.wait(self.mutex)
            except:
                # print("error")
                cap.release()
                cv2.destroyAllWindows()

class MountainClimbers(object):
    def __init__(self, workout, file):
        self.workout = workout
        self.file = file
        self.mutex = QMutex()
        self.condition = QWaitCondition()
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

        self.mutex.lock()
        self.thread = VideoThread(mutex=self.mutex, condition=self.condition)
        self.thread.workout = self.workout
        self.thread.file = self.file
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
    #
    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "MountainClimbers"))
        # self.image_label.setText(_translate("MainWindow", ""))
        # self.label.setText(_translate("MainWindow", ""))

    # @pyqtSlot(np.ndarray)
    def update_image(self, img):
        self.mutex.lock()
        try:
            qt_img = self.convert_cv_qt(img)
            self.image_label.setPixmap(qt_img)
        finally:
            self.mutex.unlock()
            self.condition.wakeAll()

    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

#     text file for correcitons

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MountainClimbers("mountainclimbers", "2.mp4")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
