# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtGui import QPixmap, QPainter, QColor, QBrush
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget
)

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_ui

class ui(QWidget):

# Sets up UI and shiii
    def __init__(self):
        super().__init__()
        self.ui = Ui_ui()
        self.ui.setupUi(self)

        # Initial image set
        img_path = os.path.join(os.path.dirname(__file__), "images/awake.jpg")
        pixmap = QPixmap(img_path)
        self.ui.sleepStatus.setScaledContents(True)
        self.ui.sleepStatus.setPixmap(pixmap)

        #initializes variables
        self.isMuted = False
        self.isDeafened = False
        self.textInput = ""
        self.output = ""
        self.sleep = False

        # Connect signals to functions
        self.ui.mute.clicked.connect(self.toggle_mute)
        self.ui.deafen.clicked.connect(self.toggle_deafen)
        self.ui.sleepMode.clicked.connect(self.sleepModel)
        self.ui.enterButton.clicked.connect(self.getTextInput)
        self.ui.showBEBox.toggled.connect(self.backEndBox)

        #connects to update_sleep_button type shii to checka nd update the text to sleeping/awake every 200ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_buttons)
        self.timer.start(200)

    # functions here

    # for toggling mute
    def toggle_mute(self, clicked):

        if self.isMuted:
            self.isMuted = False
        else:
            self.isMuted = True
        return self.isMuted
    #returns the status of isMuted, can change through main i guess

    # for toggling deafen
    def toggle_deafen(self, clicked):
        if self.isDeafened:
            self.isDeafened = False;
        else:
            self.isDeafened = True;
        return self.isDeafened
    #same idea as mute

    def getTextInput(self):
        self.textInput = self.ui.input.toPlainText()
        #sets textInput as whatever is in the input box
        self.textOutputer(textInput=self.textInput)
        #calls the textOutputer function with the textInput as an arg
        self.ui.input.clear()
        #clears the box


    def textOutputer(self, textInput):
        self.ui.output.setText(textInput)
    #prints the textInput to the output box

    def sleepModel(self, clicked):
        if  self.sleep == False:
            self.sleep = True
            return self.sleep
        else:
            self.sleep = False
            return self.sleep
        # is a clicky button that toggles sleep mode

    def backEndBox(self, checked):
        if checked:
            self.ui.backendBox.show()
        else:
            self.ui.backendBox.hide()


    #constantly checks and updates the text on the sleep button
    def update_buttons(self):
        if self.sleep:
            self.ui.sleepMode.setText("Wake")
            img_path = os.path.join(os.path.dirname(__file__), "images/sleep.png")

        else:
            self.ui.sleepMode.setText("Sleep")
            img_path = os.path.join(os.path.dirname(__file__), "images/awake.jpg")
            
        pixmap = QPixmap(img_path)
        self.ui.sleepStatus.setScaledContents(True)
        self.ui.sleepStatus.setPixmap(pixmap)

        if self.isMuted:
            self.ui.mute.setText("Unmute")

        else:
            self.ui.mute.setText("Mute")

        

        if self.isDeafened:
            self.ui.deafen.setText("Undeafen")
        else:
            self.ui.deafen.setText("Deafen")




    
#lowkey so like the variables are here we just have to integrate it into main 
# then we can like write code to stop the listing or muting mic and deafening the sound and shii
#type shiii gurticus

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = ui()
    widget.show()
    sys.exit(app.exec())

    
