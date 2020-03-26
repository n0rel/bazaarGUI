from PyQt5 import QtWidgets

import qtmodern.styles, qtmodern.windows
import threading, queue, sys, hypixelDataGetter, guiManager


def eventManager(eventQueue: queue.Queue, guiView: guiManager) -> None:
    """eventManager function proccesses events
    There are 2 events we need to watch out for
    [BOXCLICK], [ITEMINFO], [HOMEBUTTONPRESS]

    'HOMEBUTTONPRESS':
    {'EVENT': 'HOMEBUTTONPRESS', # called when the home button is pressed and we need to update and show
                                 # the home screen

     'ARGS': []                  # no arguments passed.
    }

    'BOXCLICK':
    {'EVENT': 'BOXCLICK', # called when the user clicks on an itembox (home screen boxes that display item info)

     'ARGS': [item_name]  # the name of the item the itembox is representing
    }

    'ITEMINFO':
    {'EVENT': 'ITEMINFO', # called when the hypixelDataGetter's run function returns a dataset
                          # of items from the API

     'ARGS': [[data]]     # a list of data from the Hypixel API
    }

    :param eventQueue: the eventQueue that holds incoming events
    :param guiView: the guiManager view object that manages events from and to the gui
    :return None: void function
    """

    # List to store all data, used for graphs
    data = []
    # Infinite loop that checks the event queue
    while True:
        # Get the latest updated data from the data list
        latestData = data[len(data) - 1] if len(data) > 0 else {}
        # get incoming event
        event = eventQueue.get()

        # Check event types
        if event['EVENT'] == "BOXCLICK":
            # user clicked on item box, we need to tell the view to open the specific item window
            guiView.boxEvent(event['ARGS'][0], data)

        elif event['EVENT'] == "ITEMINFO":
            # update data
            data.append(event['ARGS'][0])
            # update latestData
            latestData = data[len(data) - 1] if len(data) > 0 else {}
            # update currentHigh values (widget displayed on the right)
            guiView.window.highWidget.updateValues(latestData)

            # if we are currently viewing the home page, update the itembox's labels
            if guiView.currentView == 'home':
                guiView.window.homeWidget.updateHome(currentItem=guiView.currentItem, data=latestData)
            # else, we are on the graph page (itemView) so update that page
            else:
                item = guiView.window.itemWidget.itemViewitem
                guiView.window.itemWidget.updateItem(item, data)

            # update all graphs
            guiView.updateGraphs(data)


        elif event['EVENT'] == "HOMEBUTTONPRESS":
            # user pressed the home button, show the home page
            guiView.homeEvent(data=latestData)


"""Main Thread

Thread takes care of the running app
"""

# Create a queue to store events coming from the GUI
eventQueue = queue.Queue()

# Create a data class that will handle the hypixel API
dataClass = hypixelDataGetter.data(eventQueue=eventQueue, key='7e8355c8-a50b-4473-ba41-b03d0473a0d8')
# run the thread that every 2 mins takes data from the hypixel API
threading.Thread(target=dataClass.run).start()

# Create the QAppilication
app = QtWidgets.QApplication([])
qtmodern.styles.dark(app)
# instantiate the view object which will take care of gui and events
guiView = guiManager.view(dataClass.productIds, eventQueue)
# run the thread that will process events
threading.Thread(target=eventManager, args=(eventQueue, guiView)).start()

# run window
sys.exit(app.exec())
