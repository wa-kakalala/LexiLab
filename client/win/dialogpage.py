# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(310, 164)
        Dialog.setStyleSheet("QDialog {\n"
"    background-color:#ffffff;\n"
"    border:none;\n"
"    border-radius:10px;\n"
"}")
        self.info = QtWidgets.QLabel(Dialog)
        self.info.setGeometry(QtCore.QRect(0, 30, 281, 20))
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.info.setFont(font)
        self.info.setStyleSheet("\n"
"    font: 25 14pt \'微软雅黑 Light\';\n"
"    color: rgb(31,31,31);\n"
"    padding-left:20px; \n"
"    background-color: rgba(255, 255, 255,0);\n"
"\n"
"    border-radius:10px;\n"
"\n"
"")
        self.info.setObjectName("info")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 100, 121, 51))
        self.pushButton.setStyleSheet("QPushButton{font: 25 14pt \'微软雅黑\';\n"
"    color: rgb(255,255,255);\n"
"    margin: 10px;\n"
"    background-color: rgb(20,196,188);\n"
"\n"
"border-radius:5px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color:rgb(44 , 137 , 255);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color:rgb(14 , 135 , 228);\n"
"    padding-left:3px;\n"
"    padding-top:3px;\n"
"}\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 100, 121, 51))
        self.pushButton_2.setStyleSheet("QPushButton{font: 25 14pt \'微软雅黑\';\n"
"    color: rgb(255,255,255);\n"
"    margin: 10px;\n"
"    background-color: rgb(20,196,188);\n"
"\n"
"border-radius:5px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color:rgb(44 , 137 , 255);\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color:rgb(14 , 135 , 228);\n"
"    padding-left:3px;\n"
"    padding-top:3px;\n"
"}\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Warning"))
        self.info.setText(_translate("Dialog", "相关内容已存在，保存or丢弃？"))
        self.pushButton.setText(_translate("Dialog", "Save"))
        self.pushButton_2.setText(_translate("Dialog", "Discard"))