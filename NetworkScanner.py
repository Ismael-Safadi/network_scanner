import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow ,QLabel  , QPushButton
from PyQt5.QtCore import Qt
from Specific_ip import Specific
import qdarkstyle
import os
from Range import  Range
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        # specify  length and width for main window
        self.title = 'Network Scanner'
        self.left = 10
        self.top = 10
        self.width = 440
        self.height = 480
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.initUI()

    def initUI(self): # this function for GUI creation
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        ###########
        # main label
        self.label = QLabel('Network Scanner', self)
        self.label.setStyleSheet("font: 20pt;")
        self.label.move(100, 50)
        self.label.resize(250,50)
         ####
        # just label
        self.labe2 = QLabel('choose the way to start scan ', self)
        self.labe2.setStyleSheet("font: 13pt;")
        self.labe2.move(80, 120)
        self.labe2.resize(350, 50)
        #####
        # create button for scan specific  window
        self.button = QPushButton('Scan using specific IP address', self)
        self.button.move(50, 200)
        self.button.resize(350, 50)
        self.button.setStyleSheet("font: 10pt;")
        self.button.clicked.connect(self.on_click)
        ###############
        # create button for scan range window
        self.button2 = QPushButton('Scan using IP address range', self)
        self.button2.move(50, 300)
        self.button2.resize(350, 50)
        self.button2.setStyleSheet("font: 10pt;")
        self.button2.clicked.connect(self.on_click2)
        self.show()


    def on_click(self): # function for  Specific scan window
        self.S = Specific() # call Specific class
        self.S.show() # show the window for Specific scan
    ########
    @pyqtSlot()
    def on_click2(self):# function for  Range scan window
        self.R = Range() # call Range class
        self.R.show()# show the window for Range scan
if __name__ == '__main__':
    # exceute app
    os.environ['QT_API']='pyqt5'
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())
    ex = App()
    sys.exit(app.exec_())


# Done
