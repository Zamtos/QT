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

        self.newLetter()
        self.dLocation()
        self.s = ephem.Sun()
        self.s.compute(epoch=ephem.now())
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
        cursor.insertText("Tomasz Dróżdż", boldFormat)
        cursor.insertBlock()
        cursor.insertText("Politechnika Wrocławska", textFormat)
        cursor.insertBlock()
        cursor.insertText("Automatyka i Robotyka")
        cursor.insertBlock()
        cursor.insertText("SOLAR PANEL Program")
        cursor.setPosition(topFrame.lastPosition())
        cursor.insertText(QDate.currentDate().toString("Dziś jest: d MMMM yyyy:"),
                textFormat)
        cursor.insertText(QTime.currentTime().toString("  hh:mm:ss"), textFormat)
#        cursor.insertText(QTimer.timer("  hh:mm:ss", 1000), textFormat)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText("Wrocław: ", textFormat)
        cursor.insertText("17.03 deg; 51.10 deg", textFormat)
        cursor.insertText(",", textFormat)
        for i in range(3):
            cursor.insertBlock()
        cursor.insertText("Text", textFormat)

    def dLocation(self):
        s = ephem.Sun()
        s.compute(epoch=ephem.now())
        print("R.A.: %s DEC.: %s" % (s.a_ra, s.a_dec))
        o = ephem.Observer()
        o.lon, o.lat = '17.03333', '51.100000' # Współrzędne Wrocławia
        o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
        s.compute(o)
        hour_angle = o.sidereal_time() - s.ra
        t = ephem.hours(hour_angle + ephem.hours('12:00')).norm  # .norm for 0..24
        rad = str(ephem.hours(hour_angle + ephem.hours('12:00')).norm)
        print("HOUR ANGLE: %s SIDERAL TIME: %s" % (rad, o.sidereal_time()))


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
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newLetterAct)
#        self.fileMenu.addAction(self.DefaultAct)
        self.fileMenu.addSeparator()
        self.editMenu = self.menuBar().addMenu("&Edit")
        self.viewMenu = self.menuBar().addMenu("&View")
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Help")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

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
        self.customerList = QLabel(dock)
        self.customerList.setText((
            "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton"))
        dock.setWidget(self.customerList)
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

        dock = QDockWidget("Współrzędne", self)
        s = ephem.Sun()
        s.compute(epoch=ephem.now())
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.multiWidget3 = QWidget()
        self.vLayout3 = QGridLayout()
        self.result = QLabel(self.latlong)
        self.latitude = QLabel('Latitude')
        self.longitude = QLabel('longitude')
        self.result = QLabel('Result')
        self.rightascension = QLabel('R.A.')
        self.latitudeEdit = QTextEdit()
        self.longitudeEdit = QTextEdit()
        self.resultEdit = QTextEdit()
#        self.latitude = QTextEdit()
#        self.latitude.setFixedHeight(24)
#        self.longitude = QTextEdit()
#        self.longitude.setFixedHeight(24)
        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton3)
        self.vLayout3.addWidget(self.latitude)
        self.vLayout3.addWidget(self.latitudeEdit)
        self.vLayout3.addWidget(self.longitude)
        self.vLayout3.addWidget(self.longitudeEdit)
        self.vLayout3.addWidget(self.rightascension)
        self.vLayout3.addWidget(self.button)
        self.vLayout3.addWidget(self.result)
#        self.vLayout3.addWidget(self.resultEdit)
        self.multiWidget3.setLayout(self.vLayout3);
        dock.setWidget(self.multiWidget3);
        self.addDockWidget(Qt.RightDockWidgetArea, dock)


    def handleButton2(self):
        self.result.setText(self.latitudeEdit.toPlainText()+self.longitudeEdit.toPlainText())


    def handleButton3(self):
#        s = ephem.Sun()
#        s.compute(epoch=ephem.now())
#        print("R.A.: %s DEC.: %s" % (s.a_ra, s.a_dec))
        self.result.setText(s.ra)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
