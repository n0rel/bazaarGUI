import datetime
import queue
from Widgets import graph, MainWindow


class view():
    """guiManager's view object. Handles all events related to the GUI and the gui itself"""

    def __init__(self, listOfIds: list, eventQueue: queue.Queue):
        # create the item graphs, store them in a dataset
        self.graphs = {}
        for item in listOfIds:
            graf = graph.graph(5, 4)
            self.graphs[item] = graf

        self.currentItem = ''
        self.currentView = 'home'
        # create the MainWindow object
        self.window = MainWindow.MainWindow(listOfIds=listOfIds, eventQueue=eventQueue, graphs=self.graphs)
        # show the mainwindow
        self.window.show()

    def updateGraphs(self, data: list):
        """Function updates all graphs with their respective data

        :param data: all data saved from the Hypixel API up untill now
        :return None:
        """

        # Loop through all graphs
        for item_name, graph in self.graphs.items():
            # If there is no data, display empty data
            if len(data) == 0:
                x = []
                y = []
            else:
                # the X will be the time of each
                x = []
                # the Y will be the price
                y = []

                # loop through all dictionaries (dictionary added every 2 min)
                for dictionary in data:
                    if item_name in dictionary:
                        price = dictionary[item_name]['ppu']
                        try:
                            # check if price is Error. if it is, use the price 1 index before so it
                            # shows that the price hasn't changed
                            y.append(float(price)) if price != 'Error' else y.append(y[-1])
                            # add the time
                            x.append(datetime.datetime.fromtimestamp(dictionary[item_name]['time']).strftime("%H:%M"))
                        except IndexError:
                            # list is empty, so we don't add time nor price
                            pass

            graph.x = x
            graph.y = y
            # plot graph
            graph.plot((x, y))

    def boxEvent(self, item_name: str, data: list):
        """Function changes current page to graph page

        :param item_name: item clicked
        :param data: all data saved from the Hypixel API up untill now
        :return None:
        """
        # make sure the guiManager knows we are on the item page
        self.currentView = 'item'
        self.currentItem = item_name
        self.window.graphPage.changeItem(itemName=item_name, data=data, graph=self.graphs[item_name])
        self.window.pageWidget.setCurrentWidget(self.window.graphPage)

    def homeEvent(self, data: dict):
        """Function changes current page to home page

        :param data: all data saved from the Hypixel API up untill now
        :return:
        """
        # make sure the guiManager knows we are on the home page
        self.currentView = 'home'
        # remove current graph displayed
        self.window.graphPage.removeGraph()
        self.window.homePage.updateHome(data=data, currentItem=self.currentItem)
        self.window.pageWidget.setCurrentWidget(self.window.homePage)