import useful_functions
from PyQt5 import QtCore, QtWidgets, QtGui


class highBox(QtWidgets.QGroupBox):

    def __init__(self, id: str):
        super(highBox, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.setFixedSize(300, 65)
        self.setObjectName("highBox")
        self.boxlayout = QtWidgets.QHBoxLayout()
        # self.boxlayout.setSpacing(2)
        self.setLayout(self.boxlayout)
        # image
        qimage = useful_functions.qimage_of_item(id)
        self.imagelabel = QtWidgets.QLabel()
        self.imagelabel.setFixedSize(25, 25)
        self.imagelabel.setScaledContents(True)
        self.imagelabel.setPixmap(QtGui.QPixmap.fromImage(qimage))
        # text
        self.percentlabel = QtWidgets.QLabel(f"{id}: 0%")

        self.boxlayout.addWidget(self.imagelabel)
        self.boxlayout.addWidget(self.percentlabel)