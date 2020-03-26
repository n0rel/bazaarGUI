import queue
from PyQt5 import QtCore, QtWidgets

from Widgets.itembox import item_box


class homeWidget(QtWidgets.QScrollArea):

    def __init__(self, graphs: dict, parent: QtWidgets.QWidget = None, listOfIds: list = None,
                 eventQueue: queue.Queue = None):
        QtWidgets.QScrollArea.__init__(self, parent)
        with open('stylesheets/homePageSheet.txt', 'r') as f:
            styleSheet = f.read()

        self.graphs = graphs
        self.setStyleSheet(styleSheet)
        self.setFixedSize(1030, 700)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.qwidget = QtWidgets.QWidget()
        self.qwidget.setObjectName("QWidget")

        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setHorizontalSpacing(5)
        self.gridlayout.setVerticalSpacing(50)

        self.qwidget.setLayout(self.gridlayout)

        self.setWidget(self.qwidget)

        self.boxes = {}

        row = 0
        for num, item_name in enumerate(listOfIds):

            # Create the groupbox widget and give it a name (same as item name)
            box = item_box(item_name=item_name, eventQueue=eventQueue, graphs=self.graphs)

            self.gridlayout.addWidget(box, row, num % 3)
            self.boxes[item_name] = box
            if num % 3 == 2:
                row += 1

    def updateHome(self, data: dict, currentItem: str):
        print('updating home...')
        # check if data is empty. if it is, pass
        for item_name, box in self.boxes.items():
            if data and item_name in data:
                box.updateBox(dataset=data[item_name])
            if currentItem == item_name:
                graph = self.graphs[item_name]
                graph.homeView()
                graph.fig.set_size_inches(5, 4)
                box.box_layout.removeWidget(graph)
                box.box_layout.addWidget(graph, 3, 0, 2, 0)
