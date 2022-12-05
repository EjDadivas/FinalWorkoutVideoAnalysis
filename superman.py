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

        legCorrection = ""
        elbowCorrection = ""
        spineUpCorrection = ""
        spineDownCorrection = ""
        hipUpCorrection1 = ""
        hipUpCorrection2 = ""
        hipDownCorrection = ""

        spineDownAngle = []
        maxSpineDownAngle = {}
        spineUpAngle = []
        maxSpineUpAngle = {}

        hipBottomAngle = []
        minHipAngle = {}
        hipTopAngle = []
        maxHipAngle = {}

        startPosition = False
        while True:
            try:
                success, img = cap.read()
                img = cv2.resize(img, (1280, 720))
                img = detector.findPose(img, False)
                lmList = detector.findPosition(img, False)
    
                if len(lmList) != 0:
                    spineAngle = detector.findAngle(img, 7, 11, 23)
                    elbowAngle = detector.findAngle(img, 11, 13, 15)
                    hipAngle = detector.findAngle(img, 11, 23, 25)
                    legAngle = detector.findAngle(img, 23, 25, 27)
    
                    bar = np.interp(hipAngle, (160, 170), (100, 650))
                    per = np.interp(hipAngle, (160, 170), (100, 0))
    
                    if int(legAngle) > 150 and int(elbowAngle) > 150:
                        startPosition = True
                        """ Counter for the push elbowUp"""
                        if startPosition:
    
                            if per == 100:
                                barColor = lighterblue
                                if direction == 0:
                                    count += 0.5
                                    direction = 1
    
                            if per == 0:
                                barColor = lighterblue
                                if direction == 1:
                                    count += 0.5
                                    direction = 0
    
                            if int(count) > 0:
                                if legAngle < 150:
                                    legCorrection = "Legs are not straight"
    
                                if elbowAngle < 150:
                                    elbowCorrection = "Keep your arms straight"
    
                                """Errors | direction = 0/ going down angle"""
                                if direction == 0:
                                    spineUpAngle.append(round(spineAngle))
                                    maxSpineUpAngle[count] = []
                                    maxSpineUpAngle[count] += spineUpAngle
    
                                    hipTopAngle.append(round(legAngle))
                                    maxHipAngle[count] = []
                                    maxHipAngle[count] += hipTopAngle
    
                                for key, value in maxSpineUpAngle.items():
                                    if max(value) < 140:
                                        spineUpCorrection = "Higher"
    
                                for key, value in maxHipAngle.items():
                                    if max(value) < 140:
                                        hipUpCorrection2 = "bend your hips more"
    
                                """ERRORS direction = 1 | going elbowUp"""
                                if direction == 1:  # going elbowUp
                                    spineDownAngle.append(round(spineAngle))
                                    maxSpineDownAngle[count] = []
                                    maxSpineDownAngle[count] += spineDownAngle
    
                                    hipBottomAngle.append(round(legAngle))
                                    minHipAngle[count] = []
                                    minHipAngle[count] += hipBottomAngle
    
                                for key, value in maxSpineDownAngle.items():
                                    if max(value) < 160:
                                        spineDownCorrection = "Lower"
    
                                for key, value in minHipAngle.items():
                                    if min(value) < 160:
                                        hipDownCorrection = "Straigthen your back"
    
                    corrections = [legCorrection, elbowCorrection, spineUpCorrection, spineDownCorrection,
                                   hipUpCorrection1, hipUpCorrection2, hipDownCorrection]
                    for x, correction in enumerate(corrections):
                        cv2.putText(img, correction, (10, (int(x) * 50) + 150), cv2.FONT_HERSHEY_SIMPLEX, 1, red, 2)
    
                    cv2.rectangle(img, (1100, 100), (1175, 650), barColor, 1)
                    cv2.rectangle(img, (1100, int(bar)), (1175, 650), barColor, cv2.FILLED)
                    cv2.putText(img, f'{int(per)} %', (1100, 375), cv2.FONT_HERSHEY_PLAIN, 1.5,
                                red, 2)
    
                    cv2.rectangle(img, (5, 5), (150, 100), lighterblue, cv2.FILLED)
                    cv2.putText(img, str(int(count)), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 2,
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


class SuperMan(object):
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
    ui = SuperMan("bicyclecrunch", "1.mp4")
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    print(ui.newlocation)