from PyQt5 import QtCore, QtGui, QtWidgets
import os
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
import firebase_admin
from firebase_admin import storage as admin_storage, credentials
import shutil
config = {
    "apiKey": "AIzaSyDfsyrureSbRTR7bzrMHXD--uMHT24pmTk",
    "authDomain": "workoutvideo-3feef.firebaseapp.com",
    "projectId": "workoutvideo-3feef",
    "storageBucket": "workoutvideo-3feef.appspot.com",
    "messagingSenderId": "597298385002",
    "appId": "1:597298385002:web:896bb5fa3656bde3683a13",
    "measurementId": "G-DCY3E5Q6P4",
    "databaseURL": "",
    "serviceAccount": "test1.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
filesList = []

cred = credentials.Certificate("test1.json")
admin = firebase_admin.initialize_app(cred, {"storageBucket": "workoutvideo-3feef.appspot.com"})
bucket = admin_storage.bucket()

class Ui_MainWindow(object):
    workout = ""
    file = ""
    name = ""
    localfileName = ""
    func = None
    clicked = None
    def refresh(self):
        self.status.setText('Downloading')
        all_files = storage.list_files()
        for file in all_files:
            # try:
            fileList = os.path.normpath(file.name).split(os.path.sep)
            if len(fileList) == 6:
                # print(fileList)
                cloud_path = file.name
                # print(cloud_path)
                user, week, workout, video, category, vidFile = [fileList[i] for i in range(len(fileList))]
                # print(user, week, workout, video, category, vidFile)

                folderPath = f'New/{user}/{week}/{workout}'
                if not os.path.exists(folderPath):
                    os.makedirs(folderPath)

                # storage.child(cloud_path).download(f'{folderPath}/{vidFile}')

                filePath = f'{folderPath}/{vidFile}'
                filesList.append(filePath)
                self.status.setText(f'{filePath}  is downloaded....')
            self.status.setText('Download Success')

        file_paths = []
        for root, directories, files in os.walk("New"):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename).replace("\\", '/')
                file_paths.append(filepath)  # Add it to the list.

                self.listWidget.addItem(filepath)

    def file_clicked(self):
        item = self.listWidget.currentItem()
        self.clicked = self.listWidget.currentRow()
        filename = str(item.text())
        self.label_3.setText("File Name: " + filename)

        if filename:

            get_name = os.path.split(filename)
            self.name = get_name[1]
            self.localfileName = get_name[0]
            print(self.localfileName)

            get_file = os.path.splitext(get_name[1])
            self.file = get_file[0]

            get_workout = os.path.split(get_name[0])
            self.workout = get_workout[1]

            if self.workout == "PushUps":
                self.func = Pushups(filename, self.file)
            if self.workout == "Squats":
                self.func = WallSquat(self.workout, self.file)
            if self.workout == "Mountain_Climbers":
                self.func = MountainClimbers(self.workout, self.file)
            if self.workout == "Push_Ups":
                self.func = Pushups(filename)
            if self.workout == "Planks":
                self.func = Plank(self.workout, self.file)
            if self.workout == "Bicycle_Crunch":
                self.func = BicycleCrunch(self.workout, self.file)
            if self.workout == "Side_Lunges":
                self.func = SideLunges(self.workout, self.file)
            if self.workout == "Superman":
                self.func = SuperMan(self.workout, self.file)
            if self.workout == "Jumping_Jacks":
                self.func = JumpingJacks(self.workout, self.file)
            if self.workout == "Prisoner_Squats":
                self.func = PrisonerSquats(self.workout, self.file)
            if self.workout == "Tricep_Dips":
                self.func = TricepDips(self.workout, self.file)
            if self.workout == "Wall_Squats":
                self.func = WallSquat(self.workout, self.file)
            if self.workout == "Knee_To_Chest":
                self.func = KneeToChest(self.workout, self.file)
            if self.workout == "Cobra_Pose":
                self.func = CobraPose(self.workout, self.file)
            if self.workout == "Russian_Twist":
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
        self.status.setText('Uploading...')

        fileList2 = os.path.normpath(self.localfileName).split(os.path.sep)
        root, user, week, workout = [fileList2[i] for i in range(len(fileList2))]
        print(fileList2)

        upload_path = f'{user}/{week}/{workout}/Feedback'
        print(upload_path)
        cloudTextPath = f'{upload_path}/{self.file}.txt'
        localTextPath = f'Finished/{self.localfileName}/{self.file}.txt'

        # text = open(localTextPath).read()
        # self.label_2.setText(text)

        # storage.child(cloudTextPath).put(localTextPath)
        print(f"TextSuccess: Local: {localTextPath} || Cloud: {cloudTextPath}")


        cloudVideoPath = f'{upload_path}/{self.file}.mp4'
        localVideoPath = f'Finished/{self.localfileName}/{self.file}.mp4'
        # storage.child(cloudVideoPath).put(localVideoPath)
        print(f"Video Success: Local: {localVideoPath} || Cloud: {cloudVideoPath}")


        # deletefile = f'{user}/{week}/{workout}/Video/New/{self.file}.mp4'
        # print("Delete this file: ", deletefile)
        # blob = bucket.blob(deletefile)
        # print(blob)
        # blob.delete()
        # print('Deletion Successful')

        self.status.setText('All Uploads Successful')

        # donePath = f'Done/{self.localfileName}'
        # if not os.path.exists(donePath):
        #     os.makedirs(donePath)
        # src_path = f'{self.localfileName}/{self.file}.mp4'
        # dst_path = f'{donePath}/{self.file}.mp4'
        # # shutil.move(src_path, dst_path)
        # print(src_path)
        # print('File Moved')

        self.listWidget.takeItem(self.clicked)





    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(999, 650)
        MainWindow.setStyleSheet("background: rgb(153, 110, 180)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 470, 221, 71))
        self.pushButton.setStyleSheet("background: rgb(224, 176, 255);\n"
"font-size: 25px;\n"
"border-radius: 5px;\n"
"border: 2px solid rgb(0, 0, 0);\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.refresh)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(350, -10, 231, 51))
        self.label.setStyleSheet("font-size: 30px;\n"
"color: white;")
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(510, 150, 441, 281))
        self.scrollArea.setStyleSheet("background: white")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 439, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        """Text File"""
        self.label_2.setGeometry(QtCore.QRect(10, 3, 411, 41))
        self.label_2.setObjectName("label_2")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        """Process Button"""
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 470, 221, 71))
        self.pushButton_2.setStyleSheet("background: rgb(224, 176, 255);\n"
"font-size: 25px;\n"
"border-radius: 5px;\n"
"border: 2px solid rgb(0, 0, 0);\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openWindow)
        """Upload Button"""
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(690, 470, 221, 71))
        self.pushButton_3.setStyleSheet("background: rgb(224, 176, 255);\n"
"font-size: 25px;\n"
"border-radius: 5px;\n"
"border: 2px solid rgb(0, 0, 0);\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.uploadFirebase)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 60, 461, 51))
        self.label_3.setStyleSheet("font-size: 15px;\n"
"color: white;")
        self.label_3.setObjectName("label_3")

        """For the Status"""
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(60, 560, 841, 51))
        self.status.setStyleSheet("font-size: 15px;\n"
                                   "color: white;")
        self.status.setObjectName("status")

        """List Widget"""
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(50, 70, 401, 361))
        self.listWidget.setStyleSheet("background: white;")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemClicked.connect(self.file_clicked)


        """Menu Bar"""

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 999, 21))
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
        self.pushButton.setText(_translate("MainWindow", "REFRESH"))
        self.label.setText(_translate("MainWindow", "VIDEO ANALYSIS"))
        self.label_2.setText(_translate("MainWindow", "Text File"))
        self.pushButton_2.setText(_translate("MainWindow", "PROCESS VIDEO"))
        self.pushButton_3.setText(_translate("MainWindow", "UPLOAD"))
        self.label_3.setText(_translate("MainWindow", "File Name: "))
        self.status.setText(_translate("MainWindow", ""))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
