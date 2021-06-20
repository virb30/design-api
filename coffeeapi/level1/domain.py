class Order:
    def __init__(self, coffee='', size='', milk='', location='', id=None):
        self.id = None if id is None else int(id)
        self.coffee = coffee
        self.size = size
        self.milk = milk
        self.location = location


class DoesNotExist(Exception):
    pass


class CoffeeShop:
    def __init__(self):
        self.orders = {}

    def create(self, order):
        if order.id is None:
            order.id = len(self.orders) + 1
        self.orders[order.id] = order
        return order

    def delete(self, order):
        try:
            return self.orders.pop(order.id)
        except KeyError as e:
            raise DoesNotExist(order.id)

    def update(self, order):
        if order.id not in self.orders:
            raise DoesNotExist(order.id)

        self.orders[order.id] = order

        return order

    def read(self, id):
        id = int(id)
        try:
            return self.orders[id]
        except KeyError as e:
            raise DoesNotExist(id)