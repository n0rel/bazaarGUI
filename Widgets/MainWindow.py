import queue
from PyQt5 import QtCore, QtWidgets, QtGui

from Widgets import currentHigh, tools
from Pages import homePage, graphPage


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, graphs: dict, listOfIds: list, eventQueue: queue.Queue):
        super(MainWindow, self).__init__()

        self.eventQueue = eventQueue
        self.listOfIds = listOfIds

        self.central_widget = QtWidgets.QWidget()
        self.central_layout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        self.highWidget = currentHigh.currentHigh(ids=self.listOfIds)
        self.central_layout.addWidget(self.highWidget, 0, 2)

        self.toolWidget = tools.tools(eventQueue=self.eventQueue)
        self.central_layout.addWidget(self.toolWidget, 1, 2)

        self.pageWidget = QtWidgets.QStackedWidget()
        self.central_layout.addWidget(self.pageWidget, 0, 0, 1, 2)

        self.homePage = homePage.homeWidget(listOfIds=self.listOfIds, eventQueue=self.eventQueue, graphs=graphs)
        self.pageWidget.addWidget(self.homePage)

        self.graphPage = graphPage.graphPage()
        self.pageWidget.addWidget(self.graphPage)

        self.setObjectName("MainWindow")
        self.resize(1400, 700)
