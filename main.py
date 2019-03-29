from PyQt5.QtWidgets import (QWidget,QSlider, QApplication, QTextEdit, QFileDialog,
                             QHBoxLayout, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QIcon
import sys
from widgets import MapWidget, LogWidget, SettingsWidget

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def sendLog(self, message):
        self.log.write(message)

    def getSettings(self):
        return self.settings.getSettings()

    def logSettings(self):
        self.sendLog(self.getSettings())
        self.sendLog('map: {}'.format(self.map.getMap()))

    def initUI(self):

        self.settings = SettingsWidget()

        mapLayout = QVBoxLayout()
        self.map = MapWidget()

        mapButtons = QHBoxLayout()
        self.start = QPushButton('Start', self)
        self.stop = QPushButton('Stop', self)
        self.cont = QPushButton('Contunie', self)
        mapButtons.addWidget(self.start)
        mapButtons.addWidget(self.stop)
        mapButtons.addWidget(self.cont)

        mapLayout.addStretch(1)
        mapLayout.addWidget(self.map)
        mapLayout.addLayout(mapButtons)
        mapLayout.addStretch(1)


        self.log = LogWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.settings)
        layout.addLayout(mapLayout)
        layout.addWidget(self.log)

        self.setWindowTitle('CDUTT Local Runner')
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setLayout(layout)
        self.show()

class Dev(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global ex
        layout = QVBoxLayout()
        self.move(200, 200)
        self.setMinimumWidth(300)

        updateMapButton = QPushButton('update map', self)
        logSettingsButton = QPushButton('log settings', self)

        layout.addWidget(updateMapButton)
        layout.addWidget(logSettingsButton)

        logSettingsButton.clicked.connect(ex.logSettings)
        updateMapButton.clicked.connect(ex.map.generateRandomMap)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    dev = Dev()
    sys.exit(app.exec_())
