# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diceroller.ui'
#
# Created: Sun Oct 21 22:44:54 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(720, 644)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 541, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 691, 521))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.diceRollEquation = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.diceRollEquation.setObjectName(_fromUtf8("diceRollEquation"))
        self.horizontalLayout_3.addWidget(self.diceRollEquation)
        self.rollItButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.rollItButton.setObjectName(_fromUtf8("rollItButton"))
        self.horizontalLayout_3.addWidget(self.rollItButton)
        self.verticalLayout_11.addLayout(self.horizontalLayout_3)
        self.diceRollResults = QtGui.QPlainTextEdit(self.horizontalLayoutWidget)
        self.diceRollResults.setObjectName(_fromUtf8("diceRollResults"))
        self.verticalLayout_11.addWidget(self.diceRollResults)
        self.horizontalLayout.addLayout(self.verticalLayout_11)
        self.previousEquationsList = QtGui.QListWidget(self.horizontalLayoutWidget)
        self.previousEquationsList.setObjectName(_fromUtf8("previousEquationsList"))
        self.horizontalLayout.addWidget(self.previousEquationsList)
        self.quitButton = QtGui.QPushButton(Dialog)
        self.quitButton.setGeometry(QtCore.QRect(580, 600, 98, 27))
        self.quitButton.setObjectName(_fromUtf8("quitButton"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Diceroller", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Diceroller: The Better Dice Rolling Progam", None, QtGui.QApplication.UnicodeUTF8))
        self.rollItButton.setText(QtGui.QApplication.translate("Dialog", "Roll It!", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("Dialog", "Quit", None, QtGui.QApplication.UnicodeUTF8))

