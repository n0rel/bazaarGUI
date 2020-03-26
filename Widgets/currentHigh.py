import collections
from PyQt5 import QtCore, QtWidgets, QtGui

from Widgets import highbox


class currentHigh(QtWidgets.QScrollArea):

    def __init__(self, ids: list):
        QtWidgets.QScrollArea.__init__(self, None)

        with open('stylesheets/currentHighSheet.txt', 'r') as f:
            self.setStyleSheet(f.read())

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.qwidget = QtWidgets.QWidget()
        self.qwidget.setObjectName("QWidget")

        self.scrollLayout = QtWidgets.QVBoxLayout()
        self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)

        self.qwidget.setLayout(self.scrollLayout)


        self.boxes = {}
        self.labelImages = {}

        for id in ids:
            box = highbox.highBox(id)
            self.boxes[id] = box
            self.scrollLayout.addWidget(box)

        self.setWidget(self.qwidget)

    def updateValues(self, data: dict):
        ordered_dic = collections.OrderedDict(
            sorted(data.items(), key=lambda k: float(k[1]['percentage']), reverse=True))
        for num, (key, value) in enumerate(ordered_dic.items()):

            self.boxes[key].percentlabel.setText(f"{key}: {value['percentage']}%")
            self.scrollLayout.removeWidget(self.boxes[key])
            self.scrollLayout.insertWidget(num, self.boxes[key])

        print('finished updating high values')
