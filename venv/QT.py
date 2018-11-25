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

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDate, QFile, Qt, QTextStream, QTime, QTimer
from PySide2.QtGui import (QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from PySide2.QtWidgets import (QAction, QApplication, QDialog, QDockWidget, QFrame,
        QFileDialog, QListWidget, QMainWindow, QMessageBox, QTextEdit, QLabel, QVBoxLayout, QWidget, QPushButton, QGridLayout, QLineEdit)
from QTWindow2 import NewWindow
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
        #self.text1.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.text1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
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

        self.createActions()
        self.createMenus()
        #self.createToolBars()
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
        # zmienna = []
        # i=0
        # with open('Breslau.txt', 'r') as f:
        #     for line in f:
        #         zmienna.append(line)
        #         i=i+1
        #     print(zmienna)
        #     f = self.nameEdit.text()
        #     f = self.latitudeEdit.text()
        #     f = self.longitudeEdit.text()
        #     f = self.dateandtimeEdit.text()
        #     print(self.nameEdit.text())
        #     print(self.latitudeEdit.text())
        #     print(self.longitudeEdit.text())
        #     print(self.dateandtimeEdit.text())


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#
#         self.latlong = "0"
#         self.textEdit = QTextEdit()
#         self.setCentralWidget(self.textEdit)
#         self.createActions()
#         self.createMenus()
#         #self.createToolBars()
#         self.createStatusBar()
#         self.createDockWindows()
#         self.setWindowTitle("Panel Słoneczny")
#         self.rad = 0
#         self.o = 0
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.dLocation)
#         self.timerIsUp = False
#         self.timer2 = QTimer()
#         self.timer2.timeout.connect(self.update)
#         self.timer2.start(1000)
#         self.newLetter()
#         self.s = ephem.Sun()
#         self.o = ephem.Observer()

    def NewWindow(self):
        newWin = NewWindow()



    def newLetter(self):

        self.textEdit.clear()
        self.text2 = QLabel("<b>Domyślne Współrzędne:</b><br/>"
                            "Szerokość: 51° 06' 00''<br/>"
                            "Długość: 17° 01' 00''<br/>"
                            "(Współrzędne geograficzne Wrocławia)")

        cursor = self.textEdit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        topFrame = cursor.currentFrame()
        topFrameFormat = topFrame.frameFormat()
        topFrameFormat.setPadding(16)
        topFrame.setFrameFormat(topFrameFormat)
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
        self.text2.setText(self.nameEdit.text())
        cursor.insertText
        #self.text1.setText(self.nameEdit.text())
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
        if self.nameEdit.text():
            self.text1.setText(self.nameEdit.text())
            font03 = QFont("Arial", 16)
            font03.setBold(True)
            self.text1.setFont(font03)
            if not self.dateandtimeEdit.text():
                self.o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
        else:
            if self.dateandtimeEdit.text():
                self.o.date = self.dateandtimeEdit.text()
                self.text1.setText("<b>Obliczenia dla:</b><br/> " + self.dateandtimeEdit.text())
                font03 = QFont("Arial", 16)
                font03.setBold(True)
                self.text1.setFont(font03)
            else:
                self.o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
        #self.o.date = ephem.now()  # 00:22:07 EDT 06:22:07 UT+1
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



    def update(self):
        time = QTime.currentTime()
        self.clock.setText(QTime.currentTime().toString("hh:mm:ss"))

    def about(self):
        QMessageBox.about(self, "O Programie",
                          "<p align=justify>Program <b><i>''Panel Słoneczny''</b></i> pozwala na wyliczenie współrzędnych Słońca, "
                          "na podstawie których należy ustawić Panel. Domyślnie program startuje dla "
                          "szerokości i&nbsp;długości geograficznej Wrocławia z obecną dla użytkownika datą i godziną. "
                          "Użytkownik może podać swoją szerokość i długość geograficzną oraz swój czas i datę wpisując "
                          "w odpowiednie pola swoje dane. W polach Szerokość i Długość należy podać w stopniach dziesiętnych "
                          "W polu ''Data i Czas'' własne dane należy wpisywać zgodnie ze schematem: "
                          "rok/mies/dzień godz:min:sek (np.: 2019/02/04 14:02:03). Pisanie zer przed godzinami, minutami i sekundami "
                          "dla liczb poniżej dziesięciu nie jest wymagane (2019/02/04 14:02:03 = 2019/2/4 14:2:3)<p/>")
    def about2(self):
        QMessageBox.about(self, "Symbole i skróty",
                          "<p align=justify><b><i>Rektascensja (R.A.)</b></i> – (Right Ascension; wznoszenie proste) jest kątem dwuściennym "
                          "pomiędzy płaszczyzną koła godzinnego przechodzącego przez punkt Barana, a&nbsp;płaszczyzną koła godzinnego "
                          "danego ciała niebieskiego). <br/>"
                          "<b><i>Deklinacja (DEC.)</b></i> - kąt zawarty między płaszczyzną równika niebieskiego,"
                          "a prostą łączącą punkt na sferze niebieskiej, a środkiem sfery niebieskiej. "
                          "Deklinacja zmienia się w zakresie od 90° (biegun północny) przez 0° (równik niebieski) do -90° (biegun południowy).<br/> "
                          "<b><i>Kąt Godzinny (HOUR ANGLE)</b></i> - kąt dwuścienny zawarty pomiędzy płaszczyzną lokalnego południka "
                          "i płaszczyzną koła godzinnego danego obiektu. Kąt godzinny odmierza się w kierunku zgodnym "
                          "z dziennym ruchem sfery niebieskiej, a przyjmuje on wartości (0h,24h) lub (0°,360°) "
                          "Kąt godzinny zależy od miejsca obserwacji (ulokowania panela) i od lokalnego czasu.<br/> "
                          "<b><i>Czas Gwiazdowy (SIDERAL TIME)</b></i> - czyli kąt godzinny punktu Barana. ( Jeden z&nbsp;dwóch punktów "
                          "przecięcia się ekliptyki z równikiem niebieskim. Moment przejścia Słońca przez punkt Barana "
                          "oznacza początek astronomicznej wiosny na półkuli północnej. Dlatego nazywany jest także punktem "
                          "równonocy wiosennej.)<br/> " 
                          "<b><i>Wysokość Słońca (nad horyzontem; SUN Altitude)</b></i> - na daną chwilę wyliczona wysokość Słońca, "
                          "jeżeli jest ujemna to znaczy, że słońce jest pod horyzontem.<br/> " 
                          "<b><i>Azymut Słońca (SUN Azimuth)</b></i> - kąt dwuścienny, w programie liczy się w kierunku na wschód "
                          "(stojąc twarzą do północy w prawo; w Astronomii jest tak samo, tzn. w prawo, ale zaczyna od południka)."
                          "Azymut geograficzny i astronomiczny różni się o 180°.<p/> ")

    def createActions(self):
        # self.newLetterAct = QAction(QIcon.fromTheme('document-new', QIcon(':/images/new.png')), "&New Letter",
        #         self, shortcut=QKeySequence.New,
        #         statusTip="Create a new form letter", triggered=self.newLetter())
        self.saveAct = QAction(QIcon.fromTheme('document-save', QIcon(':/images/save.png')), "&Zapisz", self,
                               shortcut=QKeySequence.Save,
                               statusTip="Zapisz obecne współrzędne", triggered=self.save)
        self.loadAct = QAction(QtGui.QIcon(':/images/open.png'), "&Wczytaj", self,
                               shortcut=QtGui.QKeySequence.Open,
                               statusTip="Wczytaj współrzędne z pliku", triggered=self.load)
        self.aboutAct = QAction("&O Programie", self,
                                statusTip="Pokazuje pomoc dla programu",
                                triggered=self.about)
        self.aboutAct2 = QAction("&Symbole i skróty", self,
                                statusTip="Pokazuje objaśnienia używanych w programie skrótów i symboli",
                                triggered=self.about2)
        self.quitAct = QAction("&Zamknij", self, shortcut="Ctrl+Q",
                               statusTip="Zamyka aplikację", triggered=self.close)
        self.DefaultAct = QAction(QIcon.fromTheme('document-default', QIcon(':/images/def.png')), "&Rozpocznij dla domyślnej lokacji",
               self,
               statusTip="Rozpoczyna obliczenia dla domyślnej lokacji (Wrocław)",
               triggered=self.handleButton2)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newLetterAct)


    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&Plik")
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.loadAct)
        self.fileMenu.addAction(self.DefaultAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)
        self.fileMenu.addSeparator()
        self.editMenu = self.menuBar().addMenu("&Edycja")
        self.viewMenu = self.menuBar().addMenu("&Widok")
        self.menuBar().addSeparator()
        self.helpMenu = self.menuBar().addMenu("&Pomoc")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutAct2)

    def createStatusBar(self):
        self.statusBar().showMessage("Gotowy", 3000)

    def saveing(self):
        cursor = self.textEdit.textCursor()
        self.nameEdit.text()
        cursor.insertBlock()
        self.latitudeEdit.text()
        cursor.insertBlock()
        self.longitudeEdit.text()
        cursor.insertBlock()
        self.dateandtimeEdit.text()

    def save(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Zapisywanie jako", '.', "Dokumenty textowe(*.txt)")
        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Panel Słoneczny",
                                "nie mógł zapisać pliku %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        #QApplication.setOverrideCursor(Qt.WaitCursor)
        #out << self.textEdit.toPlainText()
        out <<self.nameEdit.text()+"\n"+self.latitudeEdit.text()+"\n"+self.longitudeEdit.text()+"\n"+self.dateandtimeEdit.text()
        #out << "self.text1.setText("+self.nameEdit.text()+")"
        #QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Zapisano w '%s'" % filename, 2000)

    def load(self):
        filename, _ = QFileDialog.getOpenFileName(self)

        if not filename:
            return

        file = QFile(filename)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Panel Słoneczny",
                                          "nie mógł wczytać pliku %s:\n%s." % (filename, file.errorString()))
            return

        inf = QTextStream(file)
        #QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        #with open(file, 'r') as input:
        with open('Breslau.txt', 'r') as f:
            # f = self.nameEdit.text()
            # f = self.latitudeEdit.text()
            # f = self.longitudeEdit.text()
            # f = self.dateandtimeEdit.text()
            # print(self.nameEdit.text())
            # print(self.latitudeEdit.text())
            # print(self.longitudeEdit.text())
            # print(self.dateandtimeEdit.text())
            # for line in f:
            #      print (line, end='')
            f_name = f.readline()
            #f_name = self.nameEdit.text()
            self.text1.setText(f_name)
            f_lat = f.readline()
            f_lat = self.latitudeEdit.text()
            f_lon = f.readline()
            f_lon = self.longitudeEdit.text()
            f_dnt = f.readline()
            f_dnt = self.dateandtimeEdit.text()

            # for line in f:
            #     if 'name' in line:
            #         self.text1.setText(line)
                #if 'lat' in line:


        #self.text1.setText(self.textEdit.setPlainText(inf.readAll()))
        #self.text1.setText(self.nameEdit.text())


        #QApplication.restoreOverrideCursor()

        #self.setCurrentFile(filename)

        self.statusBar().showMessage("Wczytano plik", 2000)

    def createDockWindows(self):
        # dock = QDockWidget('n', self)
        # dock.setFeatures(dock.NoDockWidgetFeatures)
        # dock.DockWidgetMovable = False
        # dock.setAllowedAreas(Qt.TopDockWidgetArea)
        # self.addDockWidget(Qt.TopDockWidgetArea, dock)

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
        font3 = QFont("Arial", 13)
        font4 = QFont("Arial", 20)
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
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())


        dock = QDockWidget("Współrzędne Geograficzne Panelu: ", self)
        s = ephem.Sun()
        s.compute(epoch=ephem.now())
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.multiWidget3 = QWidget()
        font5 = QFont("Arial", 12)
        font6 = QFont("Arial", 17)
        self.vLayout3 = QGridLayout()
        self.result = QLabel(self.latlong)
        self.name = QLabel('Nazwa')
        self.latitude = QLabel('Szerokość')
        self.longitude = QLabel('Długość')
        self.dateandtime = QLabel('Data i Czas')
        # self.result = QLabel('')
        # self.result2 = QLabel('')
        # self.result3 = QLabel('')
        self.solarpanelcor = QLabel('WSPÓŁRZĘDNE PANELU SŁONECZNEGO: ')
        self.nameEdit = QLineEdit()
        self.nameEdit.setFixedHeight(28)
        self.nameEdit.setFixedWidth(386)
        self.nameEdit.setStatusTip("Wprowadź nazwę dla konfiguracji współrzędnych i czasu")
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
        self.dateandtimeEdit.setStatusTip("Wprowadzona data powinna być w formacie: rok/mies/dzień<spacja>godz:min:sek (np.: 2022/12/4 8:12:7)")
        self.button = QPushButton('Wylicz współrzędne / Przerwij liczenie', self)
        self.button.clicked.connect(self.handleButton4)
        self.name.setFont(font5)
        self.latitude.setFont(font5)
        self.longitude.setFont(font5)
        self.dateandtime.setFont(font5)
        self.button.setFont(font6)
        self.button.setStatusTip("Rozpoczyna Obliczenia")
        # self.button.addAction(self.buttonAct)
        # self.solarpanelcor.setFont(font5)
        # self.result.setFont(font6)
        # self.result2.setFont(font6)
        # self.result3.setFont(font6)
        self.vLayout3.addWidget(self.name)
        self.vLayout3.addWidget(self.nameEdit)
        self.vLayout3.addWidget(self.latitude)
        self.vLayout3.addWidget(self.latitudeEdit)
        self.vLayout3.addWidget(self.longitude)
        self.vLayout3.addWidget(self.longitudeEdit)
        self.vLayout3.addWidget(self.dateandtime)
        self.vLayout3.addWidget(self.dateandtimeEdit)
        self.vLayout3.addWidget(self.button)
        # self.vLayout3.addWidget(self.solarpanelcor)
        # self.vLayout3.addWidget(self.result)
        # self.vLayout3.addWidget(self.result2)
        # self.vLayout3.addWidget(self.result3)
        self.multiWidget3.setLayout(self.vLayout3);
        dock.setWidget(self.multiWidget3);
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())


    def handleButton2(self):
        self.button.setStatusTip("Przerywa liczenie")
        if self.timerIsUp == False:
            self.o.lon, self.o.lat = '17.03333', '51.100000'  # Współrzędne Wrocławia
            self.text1.setText("Wrocław")
            font03 = QFont("Arial", 16)
            font03.setBold(True)
            self.text1.setFont(font03)
            self.timer.start(1000)
            self.timerIsUp = True
        else:
            self.timer.stop()
            self.timerIsUp = False
            self.button.setStatusTip("Rozpoczyna Obliczenia")

    # def handleButton2(self):
    #     print(self.nameEdit.text())
    #     print(self.latitudeEdit.text())
    #     print(self.longitudeEdit.text())
    #     print(self.dateandtimeEdit.text())


    def handleButton3(self):
        self.button.setStatusTip("Przerywa liczenie")
        if self.timerIsUp == False:
            if self.latitudeEdit.text() and self.longitudeEdit.text():
                self.o.lat = self.latitudeEdit.text()
                self.o.lon = self.longitudeEdit.text()
            if self.nameEdit.text():
                self.text1.setText(self.nameEdit.text())
                font03 = QFont("Arial", 16)
                font03.setBold(True)
                self.text1.setFont(font03)
            else:
                self.text1.setText("Wrocław")
                font03 = QFont("Arial", 16)
                font03.setBold(True)
                self.text1.setFont(font03)
                self.o.lon, self.o.lat = '17.03333', '51.100000' # Współrzędne Wrocławia
            self.timer.start(1000)
            self.timerIsUp = True
        else:
            self.timer.stop()
            self.timerIsUp = False
            self.button.setStatusTip("Rozpoczyna Obliczenia")

    def handleButton4(self):
        self.button.setStatusTip("Przerywa liczenie")
        if self.timerIsUp == False:
            #zastąpic wlasna logika
            # if self.latitudeEdit.text() and self.longitudeEdit.text():
            #     self.o.lat = self.latitudeEdit.text()
            #     self.o.lon = self.longitudeEdit.text()
            if self.nameEdit.text():
                self.text1.setText(self.nameEdit.text())
                font03 = QFont("Arial", 16)
                font03.setBold(True)
                self.text1.setFont(font03)
            else:
                if self.latitudeEdit.text() and self.longitudeEdit.text():
                    self.o.lat = self.latitudeEdit.text()
                    self.o.lon = self.longitudeEdit.text()
                    self.text1.setText("<b>Obliczenia dla:</b><br/> " + "Szerokość: " + self.latitudeEdit.text() + "°" + "  " + "Długość: " + self.longitudeEdit.text()+"°")
                    font03 = QFont("Arial", 16)
                    #font03.setBold(True)
                    self.text1.setFont(font03)
                else:
                    self.text1.setText("Wrocław")
                    font03 = QFont("Arial", 16)
                    font03.setBold(True)
                    self.text1.setFont(font03)
                    self.o.lon, self.o.lat = '17.03333', '51.100000' # Współrzędne Wrocławia
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
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
