import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# once imported it sets the plots settings
plt.rcParams.update({'font.size': 7})
plt.rcParams['xtick.color'] = '#FFFFFF'
plt.rcParams['ytick.color'] = '#FFFFFF'


class graph(FigureCanvasQTAgg):

    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_alpha(0)
        self.x = []
        self.y = []
        self.axes = self.fig.add_subplot(111)
        self.axes.patch.set_facecolor((0.69, 0.69, 0.69))

        super(graph, self).__init__(self.fig)
        self.setStyleSheet("background-color:transparent;")

    def plot(self, data: tuple):
        x, y = data
        self.axes.cla()
        self.axes.plot(x, y, color='#bf8aef')
        self.axes.patch.set_facecolor((0.69, 0.69, 0.69))
        self.draw()

    def itemView(self):
        if len(self.x) > 10:
            self.axes.set(xlim=(self.x[-10], self.x[-1]))

    def homeView(self):
        if len(self.x) > 4:
            self.axes.set(xlim=(self.x[-4], self.x[-1]))

