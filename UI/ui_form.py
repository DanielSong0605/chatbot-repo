# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_ui(object):
    def setupUi(self, ui):
        if not ui.objectName():
            ui.setObjectName(u"ui")
        ui.resize(1920, 1080)
        ui.setMinimumSize(QSize(1920, 1080))
        ui.setMaximumSize(QSize(1920, 1080))
        font = QFont()
        font.setFamilies([u"Cascadia Code"])
        font.setPointSize(12)
        ui.setFont(font)
        ui.setAutoFillBackground(False)
        ui.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"    stop:0 #F5F5F5,\n"
"    stop:1 #D3D3D3);\n"
"color: #4B4B4B;\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.output = QLabel(ui)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(10, 550, 630, 520))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        self.output.setFont(font1)
        self.output.setAutoFillBackground(False)
        self.output.setStyleSheet(u"background-color: #F8F8FF;  /* Light Gray */\n"
"color: #000000;             /* Dark Gray text */\n"
"border: 1px solid #C0C0C0;  /* Silver border */\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.output.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.output.setWordWrap(True)
        self.input = QTextEdit(ui)
        self.input.setObjectName(u"input")
        self.input.setGeometry(QRect(10, 10, 630, 520))
        self.input.setFont(font1)
        self.input.setAutoFillBackground(True)
        self.input.setStyleSheet(u"background-color: #F8F8FF;  /* Light Gray */\n"
"color: #000000;             /* Dark Gray text */\n"
"border: 1px solid #C0C0C0;  /* Silver border */\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.sleepMode = QPushButton(ui)
        self.sleepMode.setObjectName(u"sleepMode")
        self.sleepMode.setGeometry(QRect(650, 130, 310, 50))
        font2 = QFont()
        font2.setFamilies([u"Cascadia Code"])
        font2.setPointSize(30)
        self.sleepMode.setFont(font2)
        self.sleepMode.setAutoFillBackground(False)
        self.sleepMode.setStyleSheet(u"background-color: #F8F8FF;  /* Light Gray */\n"
"color: #000000;             /* Dark Gray text */\n"
"border: 1px solid #C0C0C0;  /* Silver border */\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.sleepStatus = QLabel(ui)
        self.sleepStatus.setObjectName(u"sleepStatus")
        self.sleepStatus.setGeometry(QRect(660, 250, 151, 151))
        self.sleepStatus.setAutoFillBackground(False)
        self.sleepStatus.setStyleSheet(u"background-color: #F8F8FF;  /* Light Gray */\n"
"color: #000000;             /* Dark Gray text */\n"
"border: 1px solid #C0C0C0;  /* Silver border */\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.mute = QPushButton(ui)
        self.mute.setObjectName(u"mute")
        self.mute.setGeometry(QRect(650, 70, 310, 50))
        self.mute.setFont(font2)
        self.mute.setAutoFillBackground(False)
        self.mute.setStyleSheet(u"background-color: #F8F8FF;  /* Light Gray */\n"
"color: #000000;             /* Dark Gray text */\n"
"border: 1px solid #C0C0C0;  /* Silver border */\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.deafen = QPushButton(ui)
        self.deafen.setObjectName(u"deafen")
        self.deafen.setGeometry(QRect(650, 10, 310, 50))
        font3 = QFont()
        font3.setFamilies([u"Cascadia Code"])
        font3.setPointSize(30)
        font3.setBold(False)
        self.deafen.setFont(font3)
        self.deafen.setAutoFillBackground(False)
        self.deafen.setStyleSheet(u"background-color: #F8F8FF;  /* Light Gray */\n"
"color: #000000;             /* Dark Gray text */\n"
"border: 1px solid #C0C0C0;  /* Silver border */\n"
"border-radius: 6px;\n"
"padding: 5px;")
        self.backendBox = QLabel(ui)
        self.backendBox.setObjectName(u"backendBox")
        self.backendBox.setGeometry(QRect(1280, 59, 630, 1011))
        self.backendBox.setMinimumSize(QSize(0, 6))
        self.backendBox.setAutoFillBackground(False)
        self.backendBox.setStyleSheet(u"background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"    stop:0 #252526,\n"
"    stop:1 #1e1e1e);\n"
"color: #d4d4d4;\n"
"border-radius: 5px;\n"
"padding: 6px;\n"
"\n"
"")
        self.backendBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.showBEBox = QCheckBox(ui)
        self.showBEBox.setObjectName(u"showBEBox")
        self.showBEBox.setGeometry(QRect(1280, 10, 461, 41))
        font4 = QFont()
        font4.setFamilies([u"Cascadia Code"])
        self.showBEBox.setFont(font4)
        self.showBEBox.setStyleSheet(u"QCheckBox {\n"
"    spacing: 10px;\n"
"    color: #4B4B4B;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 20px;\n"
"    height: 20px;\n"
"    border-radius: 6px;\n"
"    border: 1px solid #aaa;\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 #F5F5F5,\n"
"                                stop:1 #D3D3D3);\n"
"}\n"
"\n"
"/* Checked state */\n"
"QCheckBox::indicator:checked {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 #4B4B4B,\n"
"                                stop:1 #2E2E2E);\n"
"    image: url(:/icons/checkmark_white.svg);  /* Or use built-in checkmark if no image */\n"
"}\n"
"\n"
"/* Optional: hover effect */\n"
"QCheckBox::indicator:hover {\n"
"    border: 1px solid #888;\n"
"}")
        self.showBEBox.setChecked(True)
        self.audioInputs = QComboBox(ui)
        self.audioInputs.setObjectName(u"audioInputs")
        self.audioInputs.setGeometry(QRect(970, 10, 301, 50))
        self.audioInputs.setFont(font2)
        self.audioInputs.setAutoFillBackground(False)
        self.audioInputs.setStyleSheet(u"combo_style = \"\"\"\n"
"QComboBox {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #2d2d2d,\n"
"        stop:1 #3c3c3c);\n"
"    color: #ffffff;\n"
"    border: 1px solid #555;\n"
"    border-radius: 6px;\n"
"    padding: 5px;\n"
"}\n"
"QComboBox::drop-down {\n"
"    border-left: 1px solid #555;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1e1e1e;\n"
"    selection-background-color: #007acc;\n"
"    color: #ffffff;\n"
"}\n"
"\"\"\"\n"
"\n"
"self.ui.inputDropdown.setStyleSheet(combo_style)\n"
"self.ui.outputDropdown.setStyleSheet(combo_style)")
        self.audioInputs.setDuplicatesEnabled(True)
        self.audioOutputs = QComboBox(ui)
        self.audioOutputs.setObjectName(u"audioOutputs")
        self.audioOutputs.setGeometry(QRect(970, 70, 301, 50))
        self.audioOutputs.setFont(font2)
        self.audioOutputs.setAutoFillBackground(False)
        self.audioOutputs.setStyleSheet(u"combo_style = \"\"\"\n"
"QComboBox {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #2d2d2d,\n"
"        stop:1 #3c3c3c);\n"
"    color: #ffffff;\n"
"    border: 1px solid #555;\n"
"    border-radius: 6px;\n"
"    padding: 5px;\n"
"}\n"
"QComboBox::drop-down {\n"
"    border-left: 1px solid #555;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1e1e1e;\n"
"    selection-background-color: #007acc;\n"
"    color: #ffffff;\n"
"}\n"
"\"\"\"\n"
"\n"
"self.ui.inputDropdown.setStyleSheet(combo_style)\n"
"self.ui.outputDropdown.setStyleSheet(combo_style)")
        self.audioOutputs.setDuplicatesEnabled(True)

        self.retranslateUi(ui)

        QMetaObject.connectSlotsByName(ui)
    # setupUi

    def retranslateUi(self, ui):
        ui.setWindowTitle(QCoreApplication.translate("ui", u"ui", None))
        self.output.setText(QCoreApplication.translate("ui", u"Output", None))
        self.input.setHtml(QCoreApplication.translate("ui", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Input</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.sleepMode.setText(QCoreApplication.translate("ui", u"Sleep", None))
        self.sleepStatus.setText("")
        self.mute.setText(QCoreApplication.translate("ui", u"Mute", None))
        self.deafen.setText(QCoreApplication.translate("ui", u"Deafen", None))
        self.backendBox.setText(QCoreApplication.translate("ui", u"TextLabel", None))
        self.showBEBox.setText(QCoreApplication.translate("ui", u"Show Backend Box", None))
    # retranslateUi

