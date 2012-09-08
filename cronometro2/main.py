#!/usr/bin/env python2

import sys, os
from PyQt4 import QtCore, QtGui
from race import Ui_MainWindow
from pygame_window import PyGameWindow


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s




class Cronometro(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)

        self.cron_window = PyGameWindow()
        self.cron_window.setWindowName("Marvin")

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000/60)

        self.file_name = ""

        # procedo a conectar los SIGNALS
        QtCore.QObject.connect(self.main_window.actionOpen_Race,QtCore.SIGNAL(_fromUtf8("activated()")),self.openFile)
        QtCore.QObject.connect(self.main_window.actionSave_As,QtCore.SIGNAL(_fromUtf8("activated()")),self.saveFileAs)
        QtCore.QObject.connect(self.main_window.actionSave_Race,QtCore.SIGNAL(_fromUtf8("activated()")),self.saveFile)


        QtCore.QObject.connect(self.timer,QtCore.SIGNAL(_fromUtf8("timeout()")),self.cron_window.update)

        self.timer.start()


    def hola(self):
        print "hola estoy corriendo =)"



    def openFile(self):
        self.file_name = QtGui.QFileDialog.getOpenFileName(self,
                                    _fromUtf8("Open Race..."),
                                    _fromUtf8("~"),
                                    _fromUtf8("Race Files (*.race);;All Files (*.*)"))


    def saveFileAs(self):
        self.file_name = QtGui.QFileDialog.getSaveFileName(self,
                                    _fromUtf8("Save Race As..."),
                                    _fromUtf8("sin_titulo.race"),
                                    _fromUtf8("Race Files (*.race);;All Files (*.*)"))


    def saveFile(self):
        if self.file_name == "":
            self.saveFileAs()






if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Cron = Cronometro()
    Cron.show()
    sys.exit(app.exec_())
