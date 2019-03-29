from PyQt5.QtWidgets import (QWidget,QSlider, QApplication, QTextEdit, QFileDialog,
                             QHBoxLayout, QVBoxLayout, QPushButton, QLabel)
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QIcon
import sys, time, os, random

class MapWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.generateRandomMap()
        self.initUI()


    def initUI(self):
        self.setMinimumSize(444, 444)
        self.setMaximumSize(444, 444)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    #for development
    def generateRandomMap(self):
        materials = ['1', '2', '3', '5', '8', 'D']
        self.setMap([[random.choice(materials) for i in range(26)] for j in range(26)])

    def getMap(self):
        return self.map

    #this method will throw exception if newMap would be invalid, else set map
    def setMap(self, newMap):
        available_types  = ['1', '2', '3', '5', '8', 'D', 'P1', 'P2', 'N']
        for i in range(26):
            for j in range(26):
                if (newMap[i][j] not in available_types):
                    return 0
        self.map = newMap[:]
        self.repaint()

    #material or player number (char) to QColor
    def letterToColor(self, num):
        d = {
            '1': QColor(33, 150, 243), #углерод
            '2': QColor(255, 143, 0), #хлор
            '3': QColor(255, 202, 40), #мышьяк
            '5': QColor(255, 236, 179), #свинец
            '8': QColor(255, 64, 129) , #ртуть
            'D': QColor(100, 221, 23), #уран
            'P1': QColor(13, 71, 161), #player 1
            'P2': QColor(213, 0, 0), #player 2
            'N': QColor(117, 117, 117) #neutralized cell
        }
        if (num.upper() in d):
            return d[num.upper()]
        else:
            return QColor(255, 255, 255)

    def getCellColor(self, i, j):
        return self.letterToColor(self.map[i][j])

    def drawWidget(self, qp):
        size = self.size()

        qp.setBrush(QColor(255,255,255))
        qp.drawRect(0,0,size.width(), size.height())

        margin = 2
        padding = 2
        cell_size = 15

        for i in range(26):
            for j in range(26):
                qp.setBrush(self.getCellColor(i, j))
                qp.drawRect(margin + (cell_size+padding)*i, margin + (cell_size+padding)*j, cell_size, cell_size)

class LogWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel('Log:')
        title.setStyleSheet('QLabel { font-weight: bold; font-size: 16pt }')

        self.log = QTextEdit()
        self.log.setMinimumWidth(300)
        self.log.setReadOnly(True)

        buttons = QHBoxLayout()
        clearButton = QPushButton('Clear', self)
        saveButton = QPushButton('Save log', self)
        buttons.addWidget(clearButton)
        buttons.addWidget(saveButton)
        clearButton.clicked.connect(self.clear)
        saveButton.clicked.connect(self.save)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.log)
        layout.addLayout(buttons)
        self.setLayout(layout)

    #TODO: new methods' name
    def write(self, text):
        self.log.setText(self.log.toPlainText()+str(text)+'\n')

    def save(self):
        with open('log{}.txt'.format(int(time.time())), 'w') as f:
            f.write(self.log.toPlainText())

    def clear(self):
        self.log.setText('')

class FilePickerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #naming yopta
        button = QPushButton('Choose', self)
        button.clicked.connect(self.choose)
        self.currentLocation = QLabel('')

        self.path = None

        layout = QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.currentLocation)
        self.setLayout(layout)
        self.setMinimumWidth(250)

    def choose(self):
        path = QFileDialog.getOpenFileName(self, 'Choose strategy', '/home')
        if (len(path)>0) and path[0]:
            self.path = path[0]
            self.currentLocation.setText(os.path.basename(path[0]))

class DelayPickerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setRange(0, 100)

        self.delay = 25
        self.slider.setValue(self.delay)
        self.slider.valueChanged.connect(self.change)

        self.currentTime = QLabel('Current: {}ms'.format(self.delay))

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.currentTime)
        self.setLayout(layout)

    def change(self):
        self.delay = self.slider.value()
        self.currentTime.setText('Current: {}ms'.format(self.delay))

    def getValue(self):
        return self.delay

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel('Settings:')
        title.setStyleSheet('QLabel { font-weight: bold; font-size: 16pt }')

        botTitle = QLabel('Choose bots:')
        botTitle.setStyleSheet('QLabel {  font-size: 14pt }')

        self.bot1 = FilePickerWidget()
        self.bot2 = FilePickerWidget()

        delayTitle = QLabel('Set delay')
        delayTitle.setStyleSheet('QLabel {  font-size: 14pt }')

        self.delay = DelayPickerWidget()

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(botTitle)
        layout.addWidget(self.bot1)
        layout.addWidget(self.bot2)
        layout.addWidget(delayTitle)
        layout.addWidget(self.delay)
        layout.addStretch(1)

        self.setLayout(layout)

    def getSettings(self):
        settings = {}
        settings['delay'] = self.delay.getValue()
        settings['bot1'] = self.bot1.path
        settings['bot2'] = self.bot2.path
        return settings

