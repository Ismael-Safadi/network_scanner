import subprocess
import sys

import datetime
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox

from port_scanner import get_ports
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QMainWindow ,QLabel ,QLineEdit , QPushButton ,QPlainTextEdit
from PyQt5.QtCore import Qt
from get_mac import get_mac
from threading import Thread
class Specific(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Network Scanner'
        self.left = 10
        self.top = 10
        self.width = 440
        self.height = 680
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.initUI()
    global result_data
    result_data = ""
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.statusBar().showMessage('Message in statusbar.')
        self.textbox = QLineEdit(self)
        self.textbox.move(120, 110) # 100 == x , 200 == y
        self.textbox.resize(250, 30)
        ###############
        ###########
        self.label = QLabel('Specific IP address scanner', self)
        self.label.setStyleSheet("font: 17pt;")
        self.label.move(70, 50)
        self.label.resize(300,50)
        ################
        self.labe_from = QLabel('IP  ', self)
        self.labe_from.setStyleSheet("font: 12pt;")
        self.labe_from.move(50, 100)
        self.labe_from.resize(50, 50)
        #################

        #############
        # result
        self.label_result = QLabel('Result', self)
        self.label_result.setStyleSheet("font: 12pt;")
        self.label_result.move(50, 180)
        self.label_result.resize(60, 30)
        # text area here ....
        self.b = QPlainTextEdit(self)
        global b
        self.b.insertPlainText(result_data)
        self.b.move(50,220)
        self.b.resize(340,240)

        #####
        self.button = QPushButton('Start Scan', self)
        self.button.setToolTip('Start Scan live hosts')
        self.button.move(137, 480)
        self.button.resize(180, 50)
        self.button.setStyleSheet("font: 14pt;")
        self.button.clicked.connect(self.start_scan)
        ###############
        self.button_scan_ports = QPushButton('Scan ports', self)
        self.button_scan_ports.move(40, 550)
        self.button_scan_ports.resize(150, 50)
        self.button_scan_ports.setStyleSheet("font: 10pt;")
        self.button_scan_ports.clicked.connect(self.scan_ports)
        #################
        self.button_scan_os = QPushButton('Scan OS', self)
        self.button_scan_os.move(250, 550)
        self.button_scan_os.resize(150, 50)
        self.button_scan_os.setStyleSheet("font: 10pt;")
        self.button_scan_os.clicked.connect(self.scan_os)
        ################################
        self.button_end = QPushButton('Get report', self)
        self.button_end.move(137, 620)
        self.button_end.resize(150, 50)

        self.button_end.setStyleSheet("color: red;font: 13pt;")
        self.button_end.clicked.connect(self.end_scan)
        self.show()
    def save_data(self, data ):
        self.ip = self.textbox.text()
        path = str(self.ip) + "--" + (str(datetime.datetime.now()).replace(" ", "_").split(".")[0]).replace(":","_") + ".txt"
        r = open(path, "a")
        r.writelines(data + "\n")
        r.close()

    def is_live(self,ip):
        # the ping command itself
        CMD = subprocess.Popen("ping -n 1 "+ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        reply = CMD.stdout.read()
        print (reply)
        if "TTL" in str(reply):
            result_data= True
        else:
            result_data=False
        if "128" in str(reply):
            result_data = "windows"

        return  result_data



    def start_scan(self):
        self.ip = self.textbox.text()
        self.mac = get_mac(self.ip)
        print (self.ip)
        if self.is_live(self.ip) == True:
            status_host = self.ip+":is live"
        else:
            status_host = self.ip+":is Not live "
        print ("check done ")
        self.b.setPlainText(status_host + "\n"+ "MAC Adderss : "+str(self.mac))
        #app.quit()
        print('specific IP address')
    ########
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter port range , like 1222-1333:')

        if ok:
            return text
        else:
            return None
    def scan_ports_tread(self,ip_range):
        global  port_port
        port_port = ""
        self.ip = self.textbox.text()
        self.ports = (get_ports(self.ip , ip_range))
        for i in self.ports:
            port_port = i + ","
        print("open ports is : " ,port_port)
        self.b.setPlainText(port_port + "\n")
        print ("opent ports set to gui ")
    def scan_ports(self):
        ip_range = self.showDialog()
        if ip_range != None:
            t = Thread(target=self.scan_ports_tread,args=(ip_range,))
            t.start()
            t.join()

    @pyqtSlot()
    def scan_os(self):
        global os
        self.ip = self.textbox.text()
        if str(self.is_live(self.ip)) == "windows":
            os = "OS : Windows"
        else:
            os="OS : linux"
        print("check done ")
        self.b.setPlainText(os + "\n")
        # app.quit()


    @pyqtSlot()
    def end_scan(self):
        self.os = os
        self.ip_report = self.textbox.text()
        print ("ip done ")
        self.mac = get_mac(self.ip)
        print ("mac done ")
        print (self.os )
        self.port_port = port_port
        print(self.port_port)
        self.report_time = str(datetime.datetime.now())
        print(self.report_time)
        self.banner = ("\n"
                       "        #####################################################################################\n"
                       "        #  _   _      _                      _       _____                                  #\n"
                       "        # | \ | |    | |                    | |     / ____|                                 #\n"
                       "        # |  \| | ___| |___      _____  _ __| | __ | (___   ___ __ _ _ __  _ __   ___ _ __  #\n"
                       "        # | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ /  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__| #\n"
                       "        # | |\  |  __/ |_ \ V  V / (_) | |  |   <   ____) | (_| (_| | | | | | | |  __/ |    #\n"
                       "        # |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\ |_____/ \___\__,_|_| |_|_| |_|\___|_|    #\n"
                       "        #        * Scan report*                                                             #\n"
                       "        #####################################################################################\n"
                       "        ")

        self.final_report = (self.banner +"\n"+ "======================================="+"\n"
                             +"IP : " + str(self.ip) + "\n"+"=======================================" + "\n"
                             +"Scanning Time : "+str(self.report_time)+
                             "\n"+"======================================="
                             + "\n"+"MAC Address : " + str(self.mac)
                             + "\n" + "======================================="
                             + "\n"+str(self.os) + "\n"
                             +"======================================="
                             + "\n"+"open ports : "+str(self.port_port )
                             +"\n"+"=======================================")
        print(self.final_report )
        self.save_data(self.final_report)
        QMessageBox.about(self, "Report Done ", "scanning report is ready ")










