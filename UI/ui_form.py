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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QPushButton,
    QSizePolicy, QTextEdit, QWidget)

class Ui_ui(object):
    def setupUi(self, ui):
        if not ui.objectName():
            ui.setObjectName(u"ui")
        ui.resize(800, 600)
        self.deafen = QCheckBox(ui)
        self.deafen.setObjectName(u"deafen")
        self.deafen.setGeometry(QRect(520, 110, 75, 20))
        self.mute = QCheckBox(ui)
        self.mute.setObjectName(u"mute")
        self.mute.setGeometry(QRect(520, 130, 75, 20))
        self.output = QLabel(ui)
        self.output.setObjectName(u"output")
        self.output.setGeometry(QRect(30, 340, 461, 221))
        self.output.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.output.setWordWrap(True)
        self.input = QTextEdit(ui)
        self.input.setObjectName(u"input")
        self.input.setGeometry(QRect(10, 30, 501, 271))
        self.enterButton = QPushButton(ui)
        self.enterButton.setObjectName(u"enterButton")
        self.enterButton.setGeometry(QRect(530, 40, 75, 24))
        self.sleepMode = QPushButton(ui)
        self.sleepMode.setObjectName(u"sleepMode")
        self.sleepMode.setGeometry(QRect(520, 150, 75, 24))

        self.retranslateUi(ui)

        QMetaObject.connectSlotsByName(ui)
    # setupUi

    def retranslateUi(self, ui):
        ui.setWindowTitle(QCoreApplication.translate("ui", u"ui", None))
        self.deafen.setText(QCoreApplication.translate("ui", u"deafen", None))
        self.mute.setText(QCoreApplication.translate("ui", u"mute", None))
        self.output.setText(QCoreApplication.translate("ui", u"TextLabel", None))
        self.enterButton.setText(QCoreApplication.translate("ui", u"OK", None))
        self.sleepMode.setText(QCoreApplication.translate("ui", u"Sleep", None))
    # retranslateUi

