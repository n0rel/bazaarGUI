from PyQt5 import QtCore, QtGui, QtWidgets

from Widgets import graph
import useful_functions


class graphPage(QtWidgets.QWidget):

    def __init__(self):
        QtWidgets.QWidget.__init__(self, None)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.itemViewitem = 'NONE'

        self.image = QtWidgets.QLabel()
        self.image.setFixedSize(50, 50)
        self.image.setScaledContents(True)
        self.grid.addWidget(self.image, 0, 0)

        self.itemLabel = QtWidgets.QLabel('No item name found')
        self.itemLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.itemLabel.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold))
        self.grid.addWidget(self.itemLabel, 0, 1)

    def changeItem(self, itemName: str, data: list, graph: graph.graph):
        print('changing item')
        self.itemViewitem = itemName
        currentData = data[len(data) - 1] if len(data) > 0 else {}
        qImage = useful_functions.qimage_of_item(item_name=itemName)
        self.image.setPixmap(QtGui.QPixmap.fromImage(qImage))

        self.itemLabel.setText(itemName)

        self.graph = graph
        self.graph.itemView()
        self.graph.fig.set_size_inches(10, 6)
        self.grid.addWidget(self.graph, 1, 0, 1, 0)

    def updateItem(self, itemName: str, data: list):
        print('updating item...')
        self.itemLabel.setText(itemName)

    def removeGraph(self):
        self.grid.removeWidget(self.graph)
