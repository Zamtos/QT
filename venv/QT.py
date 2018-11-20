#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

"""PySide2 port of the widgets/mainwindows/dockwidgets example from Qt v5.x, originating from PyQt"""

from PySide2.QtCore import QDate, QFile, Qt, QTextStream, QTime, QTimer
from PySide2.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from PySide2.QtWidgets import (QAction, QApplication, QDialog, QDockWidget,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout, QLineEdit)

##import dockwidgets_rc
import datetime
import ephem

#class logika:

#        self.s = ephem.Sun()
#        self.o = ephem.Observer()
#        self.o.date = ephem.now()
#        hour_angle = 0

#    def __init__(self, lon, lat):
#        self.s.compute(self.o)
#        hour_angle = self.o.sidereal_time() - self.s.ra

#    def setLon(self, lon):
#        self.o.lon = lon
#        self.refresh()

#    def setLon(self, lat):
#        self.o.lat = lat
#        self.refresh()

#    def getRad(self):
#        return str(ephem.hours(hour_angle + ephem.hours('12:00')).norm)

#    def getDec(self):
#        return str(self.s.a_dec)

#    def getRa(self):
#        return str(self.s.a_ra)

#    def getTime(self):
#        return str(self.o.sidereal_time()

#    def refresh(self):
#        self.o.date = ephem.now()
#        self.s.compute(self.o)
#        hour_angle = self.o.sidereal_time() - self.s.ra


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.latlong = "0"
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        self.setWindowTitle("Panel Słoneczny")
        self.rad = 0
        self.o = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.dLocation)
        self.timerIsUp = False
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.update)
        self.timer2.start(1000)
        self.newLetter()
        self.s = ephem.Sun()
        self.o = ephem.Observer()

#        self.setTime()

#    def setTime(self):
#        self.label['text'] = str(datetime.datetime.now().strftime("Today is %d-%m-%Y %H:%M:%S"))
#        root.after(1000, self.setTime)
#    def showTime(self):
#        time = QTime.currentTime()
#        text = time.toString('hh:mm:ss')
#        if(time.second() % 2) == 0:
#            text = text[:2] + ' ' + text[:3]

#        self.display(text)
#        timer = QTimer(self)
#        timer.timeout.connect(self.showTime)
#        timer.start(1000)
#    def dLocation(self):
#        s = ephem.Sun()
#        s.compute(epoch=ephem.now())
#        print("R.A.: %s DEC.: %s" % (s.a_ra, s.a_dec))
#        o = ephem.Observer()
#        o.lon, o.lat = '17.03333', '51.100000' # Współrzędne Wrocławia
#        o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
#        s.compute(o)
#        hour_angle = o.sidereal_time() - sun.ra
#        t = ephem.hours(hour_angle + ephem.hours('12:00')).norm  # .norm for 0..24
#        rad = str(ephem.hours(hour_angle + ephem.hours('12:00')).norm)
#        print("HOUR ANGLE: %s SIDERAL TIME: %s" % (rad, o.sidereal_time()))
#        # print("HOUR ANGLE2: %s SIDERAL TIME: %s" % (t, o.sidereal_time()))
#        # print("HOUR ANGLE3: %s SIDERAL TIME: %s" % (hour_angle, o.sidereal_time()))
#        print("SUN Altitude: %s SUN Azimuth: %s" % (sun.alt, sun.az))
#        root.after(1000, dLocation)

    def newLetter(self):
        self.textEdit.clear()

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)
#        timer = QTimer(self)
#        timer.timeout.connect(self.showTime)
#        timer.start(1000)
        textFormat = QTextCharFormat()
        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)
        italicFormat = QTextCharFormat()
        italicFormat.setFontItalic(True)

        tableFormat = QTextTableFormat()
        tableFormat.setBorder(1)
        tableFormat.setCellPadding(16)
        tableFormat.setAlignment(Qt.AlignRight)
        cursor.insertTable(1, 1, tableFormat)
        cursor.insertText("Domyślne Współrzędne: ", boldFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Szerokość: 51° 06' 00''", textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Długość: 17° 01' 00''")
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("(Współrzędne geograficzne Wrocławia)")
        cursor.setPosition(topFrame.lastPosition())
#         cursor.insertText(QDate.currentDate().toString("Dziś jest: d MMMM yyyy:"),
#                 textFormat)
#         cursor.insertText(QTime.currentTime().toString("  hh:mm:ss"), textFormat)
# #        cursor.insertText(QTimer.timer("  hh:mm:ss", 1000), textFormat)
#         cursor.insertBlock()
#         cursor.insertBlock()
#         cursor.insertText("Wrocław: ", textFormat)
#         cursor.insertText("17.03 deg; 51.10 deg", textFormat)
#         cursor.insertText(",", textFormat)
#         for i in range(3):
#             cursor.insertBlock()
#         cursor.insertText("Text", textFormat)

    def dLocation(self):
        self.s = ephem.Sun()
        self.s.compute(epoch=ephem.now())
        self.o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
        self.s.compute(self.o)
        hour_angle = self.o.sidereal_time() - self.s.ra
        t = ephem.hours(hour_angle + ephem.hours('12:00')).norm  # .norm for 0..24
        self.rad = str(ephem.hours(hour_angle + ephem.hours('12:00')).norm)
        self.result.setText("R.A.: " + str(self.s.a_ra) + "                DEC.: " + str(self.s.a_dec))
        self.result2.setText("HOUR ANGLE: " + str(self.rad) + " SIDERAL TIME: " + str(self.o.sidereal_time()))
        self.result3.setText("SUN Altitude: " + str(self.s.alt) + "     SUN Azimuth: " + str(self.s.az))


    def update(self):
        time = QTime.currentTime()
        self.clock.setText(QTime.currentTime().toString("hh:mm:ss"))

    def createActions(self):
        self.newLetterAct = QAction(QIcon.fromTheme('document-new', QIcon(':/images/new.png')), "&New Letter",
                self, shortcut=QKeySequence.New,
                statusTip="Create a new form letter", triggered=self.newLetter)
#        self.DefaultAct = QAction(QIcon.fromTheme('document-default', QIcon(':/images/def.png')), "&Start for Default",
#                self, shortcut=QKeySequence.New,
#                statusTip="Starts program for default location (Wrocław)",
#                triggered=self.dlocation)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newLetterAct)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&Plik")
        self.fileMenu.addAction(self.newLetterAct)
#        self.fileMenu.addAction(self.DefaultAct)
        self.fileMenu.addSeparator()
        self.editMenu = self.menuBar().addMenu("&Edycja")
        self.viewMenu = self.menuBar().addMenu("&Widok")
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Pomoc")

    def createStatusBar(self):
        self.statusBar().showMessage("Gotowy")

    def createDockWindows(self):
        dock = QDockWidget("Program", self)
        dock.setFeatures(dock.NoDockWidgetFeatures)
        dock.DockWidgetMovable = False
        dock.setAllowedAreas(Qt.LeftDockWidgetArea )
        self.multiWidget = QWidget()
        font1 = QFont("Courier New", 10)
        self.title = QLabel("SOLAR PANEL Program")
        font2 = QFont("Courier New", 10)
        font2.setBold(True)
        self.author = QLabel("Tomasz Dróżdż")
        self.author.setFont(font2)
        self.other = QLabel("Politechnika Wrocławska")
        self.other2 = QLabel("Automatyka i Robotyka")
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.title)
        self.vLayout.addWidget(self.author)
        self.vLayout.addWidget(self.other)
        self.vLayout.addWidget(self.other2)
        self.multiWidget.setLayout(self.vLayout);
        dock.setWidget(self.multiWidget);
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        dock = QDockWidget("Zegar", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea )
        self.multiWidget2 = QWidget()
        font3 = QFont("Arial", 11)
        font4 = QFont("Arial", 11)
        self.date = QLabel(QDate.currentDate().toString("d MMMM yyyy:  "))
        self.clock = QLabel(QTime.currentTime().toString("hh:mm:ss"))
        self.date.setFont(font3)
        self.clock.setFont(font4)
        font4.setBold(True)
        self.vLayout2 = QVBoxLayout()
        self.vLayout2.addWidget(self.date)
        self.vLayout2.addWidget(self.clock)
        self.multiWidget2.setLayout(self.vLayout2)
        dock.setWidget(self.multiWidget2)
        # self.customerList = QLabel(dock)
        # self.date = QLabel(dock)


        # self.customerList.setText(QTime.currentTime().toString("hh:mm:ss"))
        # self.customerList.setText((
        #     "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton"))
        # dock.setWidget(self.customerList)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

#        dock = QDockWidget("Współrzędne dla domyślnej lokacji", self)
#        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
#        self.multiWidget2 = QWidget()
#        self.vLayout2 = QVBoxLayout()
#        self.result = QLabel(self.latlong)
#        self.latitude = QTextEdit()
#        self.latitude.setFixedHeight(24)
#        self.longitude = QTextEdit()
#        self.longitude.setFixedHeight(24)
#        self.button = QPushButton('Test', self)
#        self.button.clicked.connect(self.handleButton)
#        self.vLayout2.addWidget(self.latitude)
#        self.vLayout2.addWidget(self.longitude)
#        self.vLayout2.addWidget(self.button)
#        self.vLayout2.addWidget(self.result)
#        self.multiWidget2.setLayout(self.vLayout2);
#        dock.setWidget(self.multiWidget2);
#        self.addDockWidget(Qt.RightDockWidgetArea, dock)

#    def handleButton(self):
#        self.result.setText(self.latitude.toPlainText()+self.longitude.toPlainText())

        dock = QDockWidget("Współrzędne Geograficzne Panelu: ", self)
        s = ephem.Sun()
        s.compute(epoch=ephem.now())
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.multiWidget3 = QWidget()
        font5 = QFont("Arial", 10)
        font5.setBold(True)
        font6 = QFont("Arial", 10)
        self.vLayout3 = QGridLayout()
        self.result = QLabel(self.latlong)
        self.latitude = QLabel('Latitude')
        self.longitude = QLabel('Longitude')
        self.result = QLabel('')
        self.result2 = QLabel('')
        self.result3 = QLabel('')
        self.solarpanelcor = QLabel('SOLAR PANEL COORDINATES: ')
        self.latitudeEdit = QLineEdit()
        self.latitudeEdit.setFixedHeight(24)
        self.latitudeEdit.setFixedWidth(329)
        self.longitudeEdit = QLineEdit()
        self.longitudeEdit.setFixedHeight(24)
        self.longitudeEdit.setFixedWidth(329)
#        self.latitude = QTextEdit()
#        self.latitude.setFixedHeight(24)
#        self.longitude = QTextEdit()
#        self.longitude.setFixedHeight(24)
        self.button = QPushButton('Wylicz współrzędne / Przerwij liczenie', self)
        self.button.clicked.connect(self.handleButton3)
        self.solarpanelcor.setFont(font5)
        self.result.setFont(font6)
        self.result2.setFont(font6)
        self.result3.setFont(font6)
        self.vLayout3.addWidget(self.latitude)
        self.vLayout3.addWidget(self.latitudeEdit)
        self.vLayout3.addWidget(self.longitude)
        self.vLayout3.addWidget(self.longitudeEdit)
        self.vLayout3.addWidget(self.button)
        self.vLayout3.addWidget(self.solarpanelcor)
        self.vLayout3.addWidget(self.result)
        self.vLayout3.addWidget(self.result2)
        self.vLayout3.addWidget(self.result3)
#        self.vLayout3.addWidget(self.resultEdit)
        self.multiWidget3.setLayout(self.vLayout3);
        dock.setWidget(self.multiWidget3);
        self.addDockWidget(Qt.RightDockWidgetArea, dock)


    def handleButton2(self):
        self.result.setText(self.latitudeEdit.toPlainText()+self.longitudeEdit.toPlainText())


    def handleButton3(self):
        if self.timerIsUp == False:
            #zastąpic wlasna logika
            if self.latitudeEdit.text() and self.longitudeEdit.text():
                self.o.lat = self.latitudeEdit.text()
                self.o.lon = self.longitudeEdit.text()
            else:
                self.o.lon, self.o.lat = '17.03333', '51.100000' # Współrzędne Wrocławia
            self.timer.start(1000)
            self.timerIsUp = True
        else:
            self.timer.stop()
            self.timerIsUp = False
#        s = ephem.Sun()
#        s.compute(epoch=ephem.now())
#        print("R.A.: %s DEC.: %s" % (s.a_ra, s.a_dec))



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
