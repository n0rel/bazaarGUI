import requests, time, queue, threading


class data:
    """Class focuses on getting data from the Hypixel API"""

    def __init__(self, eventQueue: queue.Queue, key: str):
        """Init function"""

        self.eventQueue = eventQueue
        self.key = key
        # list of all product ID's
        self.productIds = []
        # get all product ID's
        self.get_products()
        # dict of the latest products that were updated
        self.products_latest = {}

        # Queue that will hold the item ID's coming from different threads
        self.itemQueue = queue.Queue()

    def run(self):
        """Function gets all Hypixel Bazaar products every 2 mins"""

        while True:

            # store all product ID's into a queue to be taken by threads later
            for product in self.productIds:
                self.itemQueue.put(product)

            # dictionary we fill up with item data
            data_to_send = {}
            threads = [threading.Thread(target=self.checkProduct, args=(data_to_send,)) for x in range(3)]

            # Start the threads
            for thread in threads:
                print(f'Started thread: {thread.getName()}')
                thread.start()

            # Wait for threads to finish
            for thread in threads:
                print(f'Thread {thread.getName()} finished!')
                thread.join()

            # If the length of the data to send is greater than 0 we will send it to the event queue
            if len(data_to_send) > 0:
                self.eventQueue.put({'EVENT': 'ITEMINFO', 'ARGS': [data_to_send]})

            # wait 2 min
            for i in range(120, 0, -1):
                print(f"{i}...")
                time.sleep(1)

    def checkProduct(self, toSend: dict):
        """Method processes item data and puts inside @toSend

        :param toSend: dictionary we fill up with item data
        :return None:
        """

        # While the queue of Item ID's is not empty
        while not self.itemQueue.empty():
            productId = self.itemQueue.get()
            product_data = self.get_product(product=productId)
            # if we have existing data in memory of that product, compare
            if productId in self.products_latest and product_data is not None:
                prev_product = self.products_latest[productId]

                if prev_product is not None:
                    try:
                        new_cost = product_data['sellCoins'] / product_data['sellVolume']
                        previous_cost = prev_product['sellCoins'] / prev_product['sellVolume']

                        # market price percentage
                        price_percentage = ((new_cost - previous_cost) / previous_cost) * 100
                    except ZeroDivisionError:
                        # 2 Things can cause this exception:
                        # (1) Currently nothing has been sold. This means the percentage is 0. It has not gone up nor down.
                        # (2) When dividing by the previous price, the above happens. This still means the price hasnt changed.
                        price_percentage = 0
                        new_cost = None

                    if new_cost is not None:
                        ppu = f'{new_cost:.2f}'
                    else:
                        ppu = 'Error'

                    toSend[productId] = {'ppu': ppu,
                                         'buys': str(product_data['buys']),
                                         'sells': str(product_data['sells']),
                                         'percentage': f'{price_percentage:.2f}',
                                         'time': time.time()
                                         }

            self.products_latest[productId] = product_data

    def get_products(self):
        """Get all product ID's from the Hypixel API"""

        url = f'https://api.hypixel.net/skyblock/bazaar/products?key={self.key}'
        while True:
            r = requests.get(url)
            if r.json()['success']:
                # Set the products as the gotten products
                self.productIds = r.json()['productIds']
                return
            else:
                # if we failed, print the reason (could be key throttle or the Hypixel API is down)
                print(r.json())
                # wait 10 seconds before trying again
                for i in range(10, 0, -1):
                    print(i)
                    time.sleep(1)

    def get_product(self, product: str):
        """Get the product data from the API and store it in @self.products_latest"""

        url = f'https://api.hypixel.net/skyblock/bazaar/product?key={self.key}&productId={product}'
        r = requests.get(url).json()

        if r['success']:
            week_historic = r['product_info']['week_historic']
            # Get the last updated (current) data and store it in @self.products_latest
            to_ret = week_historic[len(week_historic) - 1]
            if to_ret is not None:
                return to_ret
