import socket
import subprocess
from threading import Thread
import datetime
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMessageBox
from get_mac import get_mac
from PyQt5.QtWidgets import   QMainWindow ,QLabel ,QLineEdit , QPushButton ,QPlainTextEdit
from PyQt5.QtCore import Qt
from port_scanner import  get_ports
class Range(QMainWindow):
    def __init__(self):
        super().__init__()
        # specify  length and width for main window
        self.title = 'Network Scanner'
        self.left = 10
        self.top = 10
        self.width = 440
        self.height = 680
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.result_data = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.statusBar().showMessage('Message in statusbar.')
        self.textbox = QLineEdit(self) #text box to get start range
        self.textbox.move(120, 110)
        self.textbox.resize(250, 30)
        ###############
        self.textbox2 = QLineEdit(self) # text box to get end range
        self.textbox2.move(120, 168)  # 100 == x , 200 == y
        self.textbox2.resize(250, 30)
        ###########
        label = QLabel('IP address Range scanner', self)
        label.setStyleSheet("font: 17pt;")
        label.move(70, 50)
        label.resize(300,50)
        ################
        labe_from = QLabel('From', self)
        labe_from.setStyleSheet("font: 12pt;")
        labe_from.move(50, 100)
        labe_from.resize(50, 50)
        #################
        labe_to = QLabel('To', self)
        labe_to.setStyleSheet("font: 12pt;")
        labe_to.move(50, 160)
        labe_to.resize(50, 50)
        #############
        # result
        label_result = QLabel('Result', self)
        label_result.setStyleSheet("font: 12pt;")
        label_result.move(50, 220)
        label_result.resize(60, 30)
        # text area here ....
        self.b = QPlainTextEdit(self)
        self.b.insertPlainText("Result here .... ")
        self.b.move(50,260)
        self.b.resize(340,200)

        #####
        # button for start scanning
        button = QPushButton('Start Scan', self)
        button.setToolTip('Start Scan live hosts')
        button.move(137, 480)
        button.resize(180, 50)
        button.setStyleSheet("font: 14pt;")
        button.clicked.connect(self.start_scan)
        ###############
        # button for port scanning
        button_scan_ports = QPushButton('Scan ports', self)
        button_scan_ports.move(40, 550)
        button_scan_ports.resize(150, 50)
        button_scan_ports.setStyleSheet("font: 10pt;")
        button_scan_ports.clicked.connect(self.scan_ports)
        #################
        # buton for os scanning
        button_scan_os = QPushButton('Scan OS', self)
        button_scan_os.move(250, 550)
        button_scan_os.resize(150, 50)
        button_scan_os.setStyleSheet("font: 10pt;")
        button_scan_os.clicked.connect(self.scan_os)
        ################################
        button_end = QPushButton('Get report', self)
        button_end.move(137, 620)
        button_end.resize(150, 50)

        button_end.setStyleSheet("color: red;font: 13pt;")
        button_end.clicked.connect(self.get_report)
        self.show()


    def is_live(self,ip):
        # function is live to check if ip given in argument is live or not
        # using ICMP packet ( ping sweep )
        CMD = subprocess.Popen("ping -n 1 " + ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        reply = CMD.stdout.read()
        print(reply)
        if "TTL" in str(reply):
            self.result_data.append(ip)
        else:
            result = False

        return self.result_data

    def ipRange(self,start_ip, end_ip):
        #get ip range using start and end of the range
        start = list(map(int, start_ip.split(".")))
        end = list(map(int, end_ip.split(".")))
        temp = start
        ip_range = []

        ip_range.append(start_ip)
        while temp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i - 1] += 1
            ip_range.append(".".join(map(str, temp)))

        return ip_range
    def get_os(self,ip):
        #get operating system depends on TTL , if TTL is 128 ==> windows
        # if TTL is 64 ==> linux  ... etc ..
        self.ip = ip
        CMD = subprocess.Popen("ping -n 1 " + self.ip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        reply = CMD.stdout.read()
        if "128" in str(reply):
            self.os = "OS : Windows"
        elif "64" in str(reply) or "255" in str(reply):
            self.os="OS : nix(Linux/Unix)"
        elif "60" in str(reply):
            self.os = "OS : Mac"
        elif "254" in str(reply):
            self.os = "OS : Router/Cisco"
        return self.os
    def start_scan(self):
        self.ip_and_mac = {} # add mac addresses to dictionary to display it as scan result for live hosts
        self.start_ip = self.textbox.text() # get start range from text box
        self.end_ip = self.textbox2.text() # get end range from end box
        self.range_ips = self.ipRange(self.start_ip, self.end_ip) # passing data into iprange function
        threads = []
        counter1 = 0
        #  loop for start threads to make your scan faster
        for i in self.range_ips:
            counter1 = counter1 + 1
            i = str(i)
            t = Thread(target=self.is_live, args=(i,))
            threads.append(t)
            if counter1 >= 20: # 20 threads by once exceution
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                del threads[:]
                counter1 = 0
            print(i)
        self.result = self.result_data
        print(self.result)
        # for just for display result as string  , concatination for string then display is
        # except router ip and you computer ip
        for ip in self.result:
            if ip not in str((socket.gethostbyname_ex(socket.gethostname()))):
                self.mac = get_mac(ip)[0]
                self.ip_and_mac[str(ip)] = str(self.mac ) # except to this device ip using get ip to this device
        self.b.setPlainText(str(self.ip_and_mac ) + "\n") # display result into text area
    ########
    # this function just for make report file
    def save_data(self, data ):
        self.ip = self.textbox.text()
        path = "Scan_report-"+(str(datetime.datetime.now()).replace(" ", "_").split(".")[0]).replace(":","_") + ".txt"
        r = open(path, "a")
        r.writelines(data + "\n")
        r.close()

    # dialog for get port range for scanning
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter port range , like 1222-1333:')
        if ok:
            return text
        else:
            return None
    # function for scan ports using threads
    def scan_ports_tread(self,port_range,ip):
        global  port_port
        global all_ports_of_all_ips
        port_port = ""
        all_ports_of_all_ips = ""
        self.ip = ip
        self.ports = (get_ports(self.ip , port_range))
        for i in self.ports:
            port_port = i + ","
        print("open ports is : " ,port_port)
        all_ports_of_all_ips = all_ports_of_all_ips + str(self.ip) + "("+str(port_port) + ")"+"\n"
        self.b.setPlainText(str(self.ip) + "("+str(port_port) + ")"+"\n")


        print ("opent ports set to gui ")



    # main function for scan ports this function will exceute when hit the button (port scan)
    # after that it will open thread for exceute the previous function
    def scan_ports(self):
        port_range = self.showDialog()
        for ip in self.result:
            print(ip + ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            if port_range != None:
                t = Thread(target=self.scan_ports_tread, args=(port_range, ip,))
                t.start()
                t.join()




    # as always  for scan os
    def scan_os(self):
        self.so_result = ""
        print('IP address range')
        for i in self.result:
            self.OS= self.get_os(i)
            self.so_result+=i+"==>"+str(self.OS)+"\n"
        self.b.setPlainText(self.so_result + "\n")
    # finally get the report and save it into text file
    def get_report(self):
        self.os_report_final  = self.so_result
        print("ip done ")
        self.ip_and_mac  =self.ip_and_mac
        print(self.ip_and_mac)
        self.all_ports_of_all_ips = all_ports_of_all_ips
        print(all_ports_of_all_ips)
        self.report_time_report_final = str(datetime.datetime.now())
        print(self.report_time_report_final)
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

        self.final_report = (self.banner + "\n" + "=======================================" + "\n"
                             + "IP : " + str(self.ip_and_mac ) + "\n" + "=======================================" + "\n"
                             + "Scanning Time : " + str(self.report_time_report_final )
                             + "\n" + "======================================="
                             + "\n" + str(self.os_report_final ) + "\n"
                             + "======================================="
                             + "\n" + "open ports : " + str(self.all_ports_of_all_ips)
                             + "\n" + "=======================================")
        print(self.final_report)
        self.save_data(self.final_report)
        QMessageBox.about(self, "Report Done ", "scanning report is ready ")












