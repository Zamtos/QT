from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDate, QFile, Qt, QTextStream, QTime, QTimer
from PySide2.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from PySide2.QtWidgets import (QAction, QApplication, QDialog, QDockWidget, QFrame,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout, QLineEdit)

##import dockwidgets_rc
import datetime
import ephem

#class NewWindow(QDialog):
class NewWindow(QMainWindow):
    def __init__(self):
        super(NewWindow, self).__init__()
    # def setupUi(self, NewWindow):

        self.latlong = "0"
        self.textEdit = QTextEdit()
        self.mainWidget = QWidget()

        self.mainLayout = QVBoxLayout()
        font0 = QFont("Arial", 12)
        font0.setBold(True)
        font01 = QFont("Arial", 12)
        font02 = QFont("Arial", 12)
        self.text1 = QLabel ("<b>Domyślne Współrzędne:</b><br/>"
                             "Szerokość: 51° 06' 00''<br/>"
                             "Długość: 17° 01' 00''<br/>"
                             "(Współrzędne geograficzne Wrocławia)")
        self.solarpanelcordinates = QLabel('WSPÓŁRZĘDNE PANELU SŁONECZNEGO: ')
        self.solarpanelcordinates.setFont(font0)
        # self.solarpanelcordinates.setFrameStyle(QFrame.Box | QFrame.Sunken)
        # self.solarpanelcordinates.setMidLineWidth(6)
        self.text1.setFont(font01)
        self.text1.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.text1.setMidLineWidth(6)
        self.result4 = QLabel('')
        self.result4.setFont(font02)
        self.result4.setMidLineWidth(3)
        self.result5 = QLabel('')
        self.result5.setFont(font02)
        self.result6 = QLabel('')
        self.result6.setFont(font02)
        self.result7 = QLabel('')
        self.result7.setFont(font02)
        self.result8 = QLabel('')
        self.result8.setFont(font02)
        self.result9 = QLabel('')
        self.result9.setFont(font02)
        self.mainLayout.addWidget(self.text1)
        self.mainLayout.addWidget(self.solarpanelcordinates)
        self.mainLayout.addWidget(self.result4)
        self.mainLayout.addWidget(self.result5)
        self.mainLayout.addWidget(self.result6)
        self.mainLayout.addWidget(self.result7)
        self.mainLayout.addWidget(self.result8)
        self.mainLayout.addWidget(self.result9)
        self.mainWidget.setLayout(self.mainLayout);
        self.setCentralWidget(self.mainWidget)

        #self.createActions()
        #self.createMenus()
        #self.createToolBars()
        #self.createStatusBar()
        self.createDockWindows()
        self.setWindowTitle("Nowe Okno")
        self.rad = 0
        self.o = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.dLocation)
        self.timerIsUp = False
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.update)
        self.timer2.start(1000)
        #self.newLetter()
        self.s = ephem.Sun()
        self.o = ephem.Observer()

    def createStatusBar(self):
        self.statusBar().showMessage("Gotowy")

    def dLocation(self):
        self.s = ephem.Sun()
        self.s.compute(epoch=ephem.now())
        if self.dateandtimeEdit.text():
            self.o.date = self.dateandtimeEdit.text()
        else:
            self.o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
        self.s.compute(self.o)
        hour_angle = self.o.sidereal_time() - self.s.ra
        t = ephem.hours(hour_angle + ephem.hours('12:00')).norm  # .norm for 0..24
        self.rad = str(ephem.hours(hour_angle + ephem.hours('12:00')).norm)
        # self.result.setText("R.A.: " + str(self.s.a_ra) + "                DEC.: " + str(self.s.a_dec))
        # self.result2.setText("HOUR ANGLE: " + str(self.rad) + " SIDERAL TIME: " + str(self.o.sidereal_time()))
        # self.result3.setText("SUN Altitude: " + str(self.s.alt) + "       SUN Azimuth: " + str(self.s.az))
        self.result4.setText("R.A.: " + str(self.s.a_ra))
        self.result5.setText("DEC.: " + str(self.s.a_dec))
        self.result6.setText("HOUR ANGLE: " + str(self.rad))
        self.result7.setText("SIDERAL TIME: " + str(self.o.sidereal_time()))
        self.result8.setText("SUN Altitude: " + str(self.s.alt))
        self.result9.setText("SUN Azimuth: " + str(self.s.az))

    def createDockWindows(self):
        dock = QDockWidget("Współrzędne Geograficzne Panelu: ", self)
        s = ephem.Sun()
        s.compute(epoch=ephem.now())
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.multiWidget3 = QWidget()
        font5 = QFont("Arial", 12)
        font6 = QFont("Arial", 17)
        self.vLayout3 = QGridLayout()
        self.result = QLabel(self.latlong)
        self.latitude = QLabel('Szerokość')
        self.longitude = QLabel('Długość')
        self.dateandtime = QLabel('Data i Czas')
        self.solarpanelcor = QLabel('WSPÓŁRZĘDNE PANELU SŁONECZNEGO: ')
        self.latitudeEdit = QLineEdit()
        self.latitudeEdit.setFixedHeight(28)
        self.latitudeEdit.setFixedWidth(386)
        self.latitudeEdit.setStatusTip("Wprowadzona szerokość powinna być w stopniach dziesiętnych (np.: 51.100000)")
        self.longitudeEdit = QLineEdit()
        self.longitudeEdit.setFixedHeight(28)
        self.longitudeEdit.setFixedWidth(386)
        self.longitudeEdit.setStatusTip("Wprowadzona długość powinna być w stopniach dziesiętnych (np.: 17.03333)")
        self.dateandtimeEdit = QLineEdit()
        self.dateandtimeEdit.setFixedHeight(28)
        self.dateandtimeEdit.setFixedWidth(386)
        self.dateandtimeEdit.setStatusTip(
            "Wprowadzona data powinna być w formacie: rok/mies/dzień<spacja>godz:min:sek (np.: 2022/12/4 8:12:7)")
        self.button = QPushButton('Wylicz współrzędne / Przerwij liczenie', self)
        self.button.clicked.connect(self.handleButton3)
        self.latitude.setFont(font5)
        self.longitude.setFont(font5)
        self.dateandtime.setFont(font5)
        self.button.setFont(font6)
        self.button.setStatusTip("Rozpoczyna Obliczenia")
        self.vLayout3.addWidget(self.latitude)
        self.vLayout3.addWidget(self.latitudeEdit)
        self.vLayout3.addWidget(self.longitude)
        self.vLayout3.addWidget(self.longitudeEdit)
        self.vLayout3.addWidget(self.dateandtime)
        self.vLayout3.addWidget(self.dateandtimeEdit)
        self.vLayout3.addWidget(self.button)
        self.multiWidget3.setLayout(self.vLayout3);
        dock.setWidget(self.multiWidget3);
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        # self.viewMenu.addAction(dock.toggleViewAction())


    def handleButton3(self):
        self.button.setStatusTip("Przerywa liczenie")
        if self.timerIsUp == False:
            if self.latitudeEdit.text() and self.longitudeEdit.text():
                self.o.lat = self.latitudeEdit.text()
                self.o.lon = self.longitudeEdit.text()
            else:
                self.o.lon, self.o.lat = '17.03333', '51.100000'  # Współrzędne Wrocławia
            self.timer.start(1000)
            self.timerIsUp = True
        else:
            self.timer.stop()
            self.timerIsUp = False
            self.button.setStatusTip("Rozpoczyna Obliczenia")


#        s = ephem.Sun()
#        s.compute(epoch=ephem.now())
#        print("R.A.: %s DEC.: %s" % (s.a_ra, s.a_dec))

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    newWin = NewWindow()
    # ui = Ui_NewWindow()
    # ui.setupUi(NewWin)
    #newWin.show()
    #sys.exit(dialog.exec_())
    sys.exit(app.exec_())