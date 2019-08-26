import sys
from PyQt5.QtWidgets import QMessageBox,QApplication,QLabel,QHBoxLayout,QProgressBar,QMainWindow,QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
import time 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from crawl import CrawlerBrowser

TIME_LIMIT = 100



class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.textPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.setWindowTitle("Login")
        self.setGeometry(0,0,400,300)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.crawler = CrawlerBrowser()

        self.email = QLabel()
        self.email.setText("Email")
        self.password = QLabel()
        self.password.setText("Password")
        
        layout = QtWidgets.QVBoxLayout(self)
        self.hbox1 = QtWidgets.QHBoxLayout(self)
        self.hbox2 = QtWidgets.QHBoxLayout(self)

        self.hbox1.addWidget(self.email)
        self.hbox1.addWidget(self.textName)
        self.hbox2.addWidget(self.password)
        self.hbox2.addWidget(self.textPass)

        layout.addLayout(self.hbox1)
        layout.addLayout(self.hbox2)        
        layout.addWidget(self.buttonLogin)

 
    def handleLogin(self):
        check = self.crawler.login(self.textName.text(), self.textPass.text())
        if check:
            self.accept()
            # self.crawler.createFriendList()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')
    
class ChooseFolderLayout(QWidget):
    def __init__(self, parent):        
        super(ChooseFolderLayout, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout(self)
        self.midLayout = QHBoxLayout(self)
        self.textInfo = QLabel()
        self.textInfo.setText("Choose folder to start crawling!")
        self.midLayout.addWidget(self.textInfo)
        
        self.buttonChooseFolder = QtWidgets.QPushButton('Choose Folder', self)
        self.buttonChooseFolder.clicked.connect(self.handleChooseFolder)
        self.topLayout.addWidget(self.buttonChooseFolder)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)

        self.startButton = QPushButton('Start', self)
        self.startButton.move(0, 30)
        self.startButton.clicked.connect(self.onButtonClick)
        self.startButton.setEnabled(False)

        self.quitButton = QPushButton('Quit', self)
        self.quitButton.clicked.connect(self.quitProgram)

        self.topLayout.addWidget(self.startButton)
        self.topLayout.addWidget(self.quitButton)
        self.topLayout.addStretch(1)

        self.layout.addLayout(self.topLayout)
        self.layout.addStretch(10)
        self.layout.addLayout(self.midLayout)
        self.layout.addWidget(self.progress)

        self.setLayout(self.layout)
        


    def handleChooseFolder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            print(folder)
        self.textInfo.setText("Click start to begin!")
        self.startButton.setEnabled(True)

    def onButtonClick(self):
        ### start crawling images and save to folder
        ### replace count with the number of account in friend list
        self.textInfo.setText("Start crawling ... ")
        self.calc = External()
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def onCountChanged(self, value):
        self.progress.setValue(value)
        if self.calc.isFinished():
            self.textInfo.setText("Done!! ")


    def quitProgram(self):
        ret = QMessageBox.question(self,'', "Are you sure to stop crawling?", QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if ret == QMessageBox.Yes:
            QApplication.quit()

class External(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)

    def run(self):
        count = 0
        while count < TIME_LIMIT:
            count +=1
            time.sleep(0.2)
            self.countChanged.emit(count)
    
    def onfinish(self):
        self.finish()

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.chooseFolder = ChooseFolderLayout(self)
        self.setCentralWidget(self.chooseFolder)
        self.setWindowTitle("Crawl")
        self.setGeometry(10, 10, 450, 150)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())