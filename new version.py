import ue9
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow():
    isOn = False
    eStop = False   # Emergency stopped
    defaultIP = "10.32."

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(390, 489)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(80, 30, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.motorGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.motorGroupBox.setGeometry(QtCore.QRect(60, 190, 271, 161))
        self.motorGroupBox.setObjectName("motorGroupBox")
        self.directionPushButton = QtWidgets.QPushButton(self.motorGroupBox)
        self.directionPushButton.setGeometry(QtCore.QRect(90, 110, 110, 23))
        self.directionPushButton.setObjectName("directionPushButton")
        self.directionPushButton.setDisabled(True)
        self.startButton = QtWidgets.QPushButton(self.motorGroupBox)
        self.startButton.setDisabled(True)
        self.startButton.setGeometry(QtCore.QRect(110, 70, 75, 23))
        self.startButton.setObjectName("startButton")
        self.motorStateLabel = QtWidgets.QLabel(self.motorGroupBox)
        self.motorStateLabel.setGeometry(QtCore.QRect(130, 30, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.motorStateLabel.setFont(font)
        self.motorStateLabel.setStyleSheet("color: rgb(255, 0, 0);")
        self.motorStateLabel.setObjectName("motorStateLabel")
        self.dutyCycleGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.dutyCycleGroupBox.setGeometry(QtCore.QRect(60, 370, 271, 91))
        self.dutyCycleGroupBox.setObjectName("dutyCycleGroupBox")
        self.dutyCycleSlider = QtWidgets.QSlider(self.dutyCycleGroupBox)
        self.dutyCycleSlider.setGeometry(QtCore.QRect(60, 30, 160, 22))
        self.dutyCycleSlider.setMinimum(0)
        self.dutyCycleSlider.setMaximum(65535)
        self.dutyCycleSlider.setSliderPosition(0)
        self.dutyCycleSlider.setOrientation(QtCore.Qt.Horizontal)
        self.dutyCycleSlider.setTickInterval(655.36)
        self.dutyCycleSlider.setObjectName("dutyCycleSlider")
        self.dutyCycleSlider.setDisabled(True)
        self.dutyCycleLabel = QtWidgets.QLabel(self.dutyCycleGroupBox)
        self.dutyCycleLabel.setGeometry(QtCore.QRect(80, 60, 101, 16))
        self.dutyCycleLabel.setObjectName("dutyCycleLabel")
        self.dutyCycleLabel.setText("Duty Cycle: 0%")
        self.ipAddressGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.ipAddressGroupBox.setGeometry(QtCore.QRect(60, 80, 271, 101))
        self.ipAddressGroupBox.setObjectName("ipAddressGroupBox")
        self.ipEdiText = QtWidgets.QLineEdit(self.ipAddressGroupBox)
        self.ipEdiText.setGeometry(QtCore.QRect(100, 40, 161, 31))
        self.ipEdiText.setText(self.defaultIP)
        self.connectButton = QtWidgets.QPushButton(self.ipAddressGroupBox)
        self.connectButton.setGeometry(QtCore.QRect(20, 43, 75, 23))
        self.connectButton.setObjectName("connectButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

#        CLICK EVENTS
        self.startButton.clicked.connect(self.motorStart)
        self.directionPushButton.clicked.connect(self.motorDirection)
        self.dutyCycleSlider.valueChanged.connect(self.pwm)
        self.connectButton.clicked.connect(self.connectLabJack)
        self.ipEdiText.returnPressed.connect(self.connectButton.click)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Motor Driver Interface"))
        self.titleLabel.setText(_translate("MainWindow", "Motor Driver Interface"))
        self.motorGroupBox.setTitle(_translate("MainWindow", "Motor Control"))
        self.directionPushButton.setText(_translate("MainWindow", "Clock Wise"))
        self.startButton.setText(_translate("MainWindow", "Start Motor"))
        self.motorStateLabel.setText(_translate("MainWindow", "OFF"))
        self.dutyCycleGroupBox.setTitle(_translate("MainWindow", "Duty Cycle"))
        self.dutyCycleLabel.setText(_translate("MainWindow", "Duty Cycle: 0%"))
        self.ipAddressGroupBox.setTitle(_translate("MainWindow", "LabJack IP Address"))
        self.connectButton.setText(_translate("MainWindow", "Connect"))

    def motorStart(self):
        if not self.eStop:                                   # check if emergency stopped
            self.motorStateLabel.setStyleSheet("color: rgb(62, 255, 68);")
            self.motorStateLabel.setText("ON")
            self.dutyCycleSlider.setEnabled(True)
            self.startButton.setDisabled(True)
            self.myUE9.timerCounter(TimerClockBase=1, TimerClockDivisor=1, Timer0Mode=0, NumTimersEnabled=1, UpdateConfig=1, Timer0Value=65535-self.dutyCycleSlider.value())
            self.isOn = True
        else:
            print("Emergency stopped: Do the password stuff")

    def motorStop(self):
        self.myUE9.timerCounter(UpdateConfig=1)             # disables PWM timer
        self.isOn = False
        self.motorStateLabel.setStyleSheet("color: rgb(255, 0, 0);")
        self.motorStateLabel.setText("OFF")
        self.startButton.setEnabled(True)

    def checkInputs(self):
        self.checking = True                                # check if already running check
        result = self.myUE9.feedback()                      # get inputs
        if result["FIOState"] & int('0b100', 2) == 0:       # reset button pressed
            print("Reset button pressed: Do reset stuff")
        if result["FIOState"] & int('0b1000', 2) == 0:      # emergency stop pressed
            self.motorStop()
            self.eStop = True
        QtCore.QTimer.singleShot(100, self.checkInputs)     # call checkInputs after a while

    def motorDirection(self):
        result = self.myUE9.feedback()                      # check current direction
        if result["FIOState"] & int('0b10', 2) == 0:        # if CW, change to CCW
            state = 0b10
            self.directionPushButton.setText("Counter Clock Wise")
        else:
            state = 0b00
            self.directionPushButton.setText("Clock Wise")
        self.myUE9.feedback(FIOMask=0b10, FIODir=0b11, FIOState=state)

    def pwm(self):
        dutyCycle = str(int((self.dutyCycleSlider.value()/65535)*100))
        self.dutyCycleLabel.setText("Duty Cycle: " + dutyCycle + "%")
        if self.isOn:                                       # if on, change PWM
            self.myUE9.timerCounter(TimerClockBase=1, TimerClockDivisor=1, Timer0Mode=0, NumTimersEnabled=1, UpdateConfig=1, Timer0Value=65535-self.dutyCycleSlider.value())

    def connectLabJack(self):
        try:
            self.myUE9 = ue9.UE9(ethernet=True, ipAddress=self.ipEdiText.text())
            self.motorStateLabel.setText("OFF")
            self.startButton.setEnabled(True)
            self.directionPushButton.setEnabled(True)
            self.dutyCycleSlider.setEnabled(True)
            self.ipEdiText.setText(self.defaultIP)
            if not self.checking:                           # if not checking inputs, start checking
                self.checkInputs()
        except:
            print("ERROR: LabJack not found")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)                # fixes kernel crash somehow
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
