import queue
from PyQt5 import QtCore, QtGui, QtWidgets

class tools(QtWidgets.QWidget):

    def __init__(self, eventQueue: queue.Queue):
        QtWidgets.QWidget.__init__(self, None)
        self.setFixedHeight(50)
        self.eventQueue = eventQueue

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.homeButton = QtWidgets.QPushButton('Home')
        self.homeButton.clicked.connect(self.clicked)
        # TODO: add icon for home button
        self.layout.addWidget(self.homeButton)

    def clicked(self):
        self.eventQueue.put({'EVENT': 'HOMEBUTTONPRESS', 'ARGS': []})

