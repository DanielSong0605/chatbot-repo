# This Python file uses the following encoding: utf-8
import sys
import os
from PySide6.QtGui import QPixmap, QPainter, QColor, QBrush, QKeyEvent
from PySide6.QtCore import QTimer, Qt, QEvent
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
    def __init__(self, inputList, outputList, parent=None, on_enter=None):
        super().__init__(parent)

        self.ui = Ui_ui()
        self.ui.setupUi(self)
        self.ui.input.installEventFilter(self)
        self.inputList = inputList
        self.outputList = outputList
        self.on_enter = on_enter

        #initializes variables
        self.isMuted = False
        self.isDeafened = False
        self.textInput = ""
        self.output = ""
        self.sleep = True
        self.BEBoxOutput = ""
        self.inputDevice = ""
        self.outputDevice = ""

        # Connect signals to functions
        self.ui.mute.clicked.connect(self.toggle_mute)
        self.ui.deafen.clicked.connect(self.toggle_deafen)
        self.ui.sleepMode.clicked.connect(self.sleepModel)
        self.ui.showBEBox.toggled.connect(self.backEndBox)
        self.ui.audioInputs.addItems(self.inputList)
        self.ui.audioOutputs.addItems(self.outputList)
        self.ui.audioInputs.currentTextChanged.connect(self.set_input_device)
        self.ui.audioOutputs.currentTextChanged.connect(self.set_output_device)

        #set state of ai
        self.state = "sleeping"  # or "listening", "talking"
        self.volume = 0.0  # Range: 0.0 to 100.0
        self.pulse_radius = 0.0

        #creates the pulsing motion type shii
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

        #connects to update_sleep_button type shii to checka nd update the text to sleeping/awake every 200ms
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_buttons(self.BEBoxOutput))
        self.timer.start(30)

    #for the ai circle

    def set_state(self, state):
        self.state = state
        self.update()

    def update_volume(self, volume):
        self.volume = min(max(volume, 0.0), 100.0)

    def animate(self):
        # Animate outer pulse if talking
        if self.state == "talking":
            self.pulse_radius = 30 + (self.volume / 3)  # e.g. 30–60px range
        else:
            self.pulse_radius = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Sizes
        w = self.width()
        h = self.height()
        center = self.rect().center()
        base_radius = min(w, h) / 6
        bg_radius = base_radius * 2

        # Draw background circle (light gray)
        painter.setBrush(QColor("#E0E0E0"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, bg_radius, bg_radius)

        # Draw pulsating red circle (only when talking)
        if self.state == "talking":
            painter.setBrush(QColor(255, 0, 0, 80))  # Transparent red
            painter.drawEllipse(center, self.pulse_radius, self.pulse_radius)

        # Draw central circle based on state
        color_map = {
            "sleeping": "#2E2E2E",  # Dark gray
            "listening": "#0080FF",  # Blue
            "talking": "#FF0000"    # Red
        }



        painter.setBrush(QColor(color_map.get(self.state, "#2E2E2E")))
        painter.drawEllipse(center, base_radius, base_radius)


    # functions here

    def eventFilter(self, obj, event):
        if obj == self.ui.input and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() != Qt.ShiftModifier:
                    self.getTextInput()  # directly call the function you want
                    return True  # suppress default enter/newline
        return super().eventFilter(obj, event)

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
            self.set_state("sleeping")
            return self.sleep

        else:
            self.sleep = False
            self.set_state("listening")
            return self.sleep


        # is a clicky button that toggles sleep mode

    def backEndBox(self, checked):
        if checked:
            self.ui.backendBox.show()
        else:
            self.ui.backendBox.hide()


    def set_input_device(self, device_name):
        self.intputDevice = device_name
        print(f"Selected input device: {device_name}")
        return self.intputDevice

    def set_output_device(self, device_name):
        self.outputDevice = device_name
        print(f"Selected output device: {device_name}")
        return self.outputDevice


    #constantly checks and updates stuff on the sleep button
    def update_buttons(self, BEBoxOutput):
        self.ui.backendBox.setText(BEBoxOutput)

        if self.sleep:
            self.ui.sleepMode.setText("Wake")


        else:
            self.ui.sleepMode.setText("Sleep")

            

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
    widget = ui(["hi", "bye"], ["1", "2"])
    widget.show()
    sys.exit(app.exec())

    
