# Form implementation generated from reading ui file 'ui/foobar.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_foobarMainWindow(object):
    def setupUi(self, foobarMainWindow):
        foobarMainWindow.setObjectName("foobarMainWindow")
        foobarMainWindow.resize(727, 567)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(foobarMainWindow.sizePolicy().hasHeightForWidth())
        foobarMainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=foobarMainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.a_horizontalLayout = QtWidgets.QHBoxLayout()
        self.a_horizontalLayout.setObjectName("a_horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setMaximumSize(QtCore.QSize(240, 16777215))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.a_horizontalLayout.addWidget(self.tableWidget)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.a_horizontalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout.addLayout(self.a_horizontalLayout)
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.btnPlay = QtWidgets.QPushButton(parent=self.frame)
        self.btnPlay.setObjectName("btnPlay")
        self.gridLayout.addWidget(self.btnPlay, 0, 1, 1, 1)
        self.btnRandQuote = QtWidgets.QPushButton(parent=self.frame)
        self.btnRandQuote.setObjectName("btnRandQuote")
        self.gridLayout.addWidget(self.btnRandQuote, 0, 2, 1, 1)
        self.btnQuit = QtWidgets.QPushButton(parent=self.frame)
        self.btnQuit.setObjectName("btnQuit")
        self.gridLayout.addWidget(self.btnQuit, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        foobarMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=foobarMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 727, 24))
        self.menubar.setObjectName("menubar")
        foobarMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=foobarMainWindow)
        self.statusbar.setObjectName("statusbar")
        foobarMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(foobarMainWindow)
        QtCore.QMetaObject.connectSlotsByName(foobarMainWindow)

    def retranslateUi(self, foobarMainWindow):
        _translate = QtCore.QCoreApplication.translate
        foobarMainWindow.setWindowTitle(_translate("foobarMainWindow", "MainWindow"))
        self.btnPlay.setText(_translate("foobarMainWindow", "Play"))
        self.btnRandQuote.setText(_translate("foobarMainWindow", "Random"))
        self.btnQuit.setText(_translate("foobarMainWindow", "Quit"))
