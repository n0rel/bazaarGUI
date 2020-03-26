import useful_functions, queue
from PyQt5 import QtCore, QtWidgets, QtGui

class item_box(QtWidgets.QGroupBox):

    def __init__(self, graphs: dict, item_name: str, eventQueue: queue.Queue) -> None:
        super(item_box, self).__init__()
        self.graphs = graphs
        self.eventQueue = eventQueue
        self.item_name = item_name
        self.setObjectName("itemBox")
        self.setup()

    def setup(self) -> None:
        self.setFixedSize(300, 300)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))

        # create layout
        self.box_layout = QtWidgets.QGridLayout(self)

        self.nameLabel = QtWidgets.QLabel(self.item_name)
        self.nameLabel.setObjectName("nameLabel")
        # self.setGeometry(0, 0, 300, 50)
        self.box_layout.addWidget(self.nameLabel, 0, 0, 1, 2)

        qImage = useful_functions.qimage_of_item(self.item_name)
        item_image = QtWidgets.QLabel()
        item_image.setFixedSize(100, 100)
        item_image.setText("")
        item_image.setPixmap(QtGui.QPixmap.fromImage(qImage))
        item_image.setScaledContents(True)
        item_image.setObjectName("item_image")
        self.box_layout.addWidget(item_image, 1, 0)

        # percentage (if the price went up or down)
        self.percentage = QtWidgets.QLabel()
        self.percentage.setObjectName("percentage")
        self.percentage.setFixedSize(75, 25)
        self.percentage.setAlignment(QtCore.Qt.AlignCenter)
        self.percentage.setText("percentage")
        self.percentage.setProperty("rising", True)
        self.box_layout.addWidget(self.percentage, 2, 0)

        # create a label that will display the price per unit
        self.ppu = QtWidgets.QLabel()
        self.ppu.setObjectName("ppu")
        self.ppu.setText("Price Per Unit")
        self.box_layout.addWidget(self.ppu, 1, 1)

        # current instant buy quantity
        self.buys = QtWidgets.QLabel()
        self.buys.setObjectName("buys")
        self.buys.setText("buys")
        self.box_layout.addWidget(self.buys, 2, 1)

        # current instant sell quantity
        self.sells = QtWidgets.QLabel()
        self.sells.setObjectName("sells")
        self.sells.setText("sells")
        self.box_layout.addWidget(self.sells, 2, 2)

        self.box_layout.addWidget(self.graphs[self.item_name], 3, 0, 2, 0)

    def updateBox(self, dataset: dict) -> None:
        self.ppu.setText(dataset['ppu'])
        self.buys.setText(dataset['buys'])
        self.sells.setText(dataset['sells'])
        self.percentage.setText(dataset['percentage'])

        # set percentage propert
        if float(dataset['percentage']) < 0:
            self.percentage.setProperty("rising", False)
        else:
            self.percentage.setProperty("rising", True)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton:
            self.eventQueue.put({'EVENT': 'BOXCLICK', 'ARGS': [self.item_name]})
