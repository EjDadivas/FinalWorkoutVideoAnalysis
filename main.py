import os.path
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import pyrebase
from mountainclimbers import MountainClimbers
from pushups import Pushups
from plank import Plank
from bicyclecrunch import BicycleCrunch
from sidelunges import SideLunges
from superman import SuperMan
from jumpingjacks import JumpingJacks
from prisonsquats import PrisonerSquats
from tricepdips import TricepDips
from wallsquat import WallSquat
from kneetochest import KneeToChest
from cobrapose import CobraPose
from russiantwist import RussianTwist


config = {
    "apiKey": "AIzaSyDfsyrureSbRTR7bzrMHXD--uMHT24pmTk",
    "authDomain": "workoutvideo-3feef.firebaseapp.com",
    "projectId": "workoutvideo-3feef",
    "storageBucket": "workoutvideo-3feef.appspot.com",
    "messagingSenderId": "597298385002",
    "appId": "1:597298385002:web:896bb5fa3656bde3683a13",
    "measurementId": "G-DCY3E5Q6P4",
    "databaseURL": ""
    }

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
class Ui_MainWindow(QMainWindow):
    # def __init__(self):
    #     super(Ui_MainWindow, self).__init__()
    workout = ""
    file = ""
    name = ""
    func = None
    def clicker(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Files", "C:\\Users\\ASUS\\Desktop\\Self-Study\\AAAA-Final-Thesis\\Videos", "All Files (*);;VideoFiles (*.mp4)")
        if fileName:
            # print(fileName)
            get_name = os.path.split(fileName)
            self.name = get_name[1]

            get_file= os.path.splitext(get_name[1])
            self.file = get_file[0]

            get_workout = os.path.split(get_name[0])
            self.workout = get_workout[1]
            print("folder: ", self.workout, "\nwithout extension:", self.file,
                  "\nfull filename:", self.name)

            if self.workout == "mountainclimbers":
                self.func = MountainClimbers(self.workout, self.file)
            if self.workout == "pushups":
                self.func = Pushups(self.workout, self.file)
            if self.workout == "plank":
                self.func = Plank(self.workout, self.file)
            if self.workout == "bicyclecrunch":
                self.func = BicycleCrunch(self.workout, self.file)
            if self.workout == "sidelunges":
                self.func = SideLunges(self.workout, self.file)
            if self.workout == "superman":
                self.func = SuperMan(self.workout, self.file)
            if self.workout == "jumpingjacks":
                self.func = JumpingJacks(self.workout, self.file)
            if self.workout == "prisonersquats":
                self.func = PrisonerSquats(self.workout, self.file)
            if self.workout == "tricep":
                self.func = TricepDips(self.workout, self.file)
            if self.workout == "wallsquats":
                self.func = WallSquat(self.workout, self.file)
            if self.workout == "kneetochest":
                self.func = KneeToChest(self.workout, self.file)
            if self.workout == "cobrapose":
                self.func = CobraPose(self.workout, self.file)
            if self.workout == "russiantwist":
                self.func = RussianTwist(self.workout, self.file)

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = self.func
        self.ui.setupUi(self.window)
        try:
            self.window.show()
        except:
            self.window.close()


    def uploadFirebase(self):
        try:
            cloudTextPath = "test-text/" + self.workout + '/' + self.file
            localTextPath = f"Finished/{self.workout}_{self.file}.txt"
            print(localTextPath)
            storage.child(cloudTextPath).put(localTextPath)

            cloudPicPath = "test-pics/" + self.workout + '/' + self.file
            localPicPath = f"Finished/{self.workout}_{self.file}.jpg"
            print(localPicPath)
            storage.child(cloudPicPath).put(localPicPath)
            print("success")
        except:
            print("file cannot be found")
            print(localPicPath, localTextPath)

    # upload txt
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(300, 10, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.header.setFont(font)
        self.header.setObjectName("header")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 100, 551, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clicker())
        self.button.setGeometry(QtCore.QRect(10, 90, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.button.setFont(font)
        self.button.setObjectName("button")
        self.processButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openWindow())
        self.processButton.setGeometry(QtCore.QRect(80, 310, 181, 81))
        self.processButton.setObjectName("processButton")
        self.uploadButton = QtWidgets.QPushButton(self.centralwidget,  clicked=lambda: self.uploadFirebase())
        self.uploadButton.setGeometry(QtCore.QRect(310, 310, 191, 81))
        self.uploadButton.setObjectName("uploadButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.header.setText(_translate("MainWindow", "Choose File"))
        self.label.setText(_translate("MainWindow", "File Name"))
        self.button.setText(_translate("MainWindow", "CHOOSE FILE"))
        self.processButton.setText(_translate("MainWindow", "PROCESS ANALYSIS"))
        self.uploadButton.setText(_translate("MainWindow", "UPLOAD ANALYSIS"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
