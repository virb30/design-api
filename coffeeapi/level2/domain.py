from enum import Enum, auto


def now():
    from django.utils.datetime_safe import datetime
    return datetime.now()


class Status(Enum):
    Placed = auto()
    Paid = auto()
    Served = auto()
    Collected = auto()


class Order:
    def __init__(self, coffee='', size='', milk='', location='', id=None, created_at=None, status=None):
        self.id = None if id is None else int(id)
        self.coffee = coffee
        self.size = size
        self.milk = milk
        self.location = location
        self.created_at = now() if created_at is None else created_at
        self.status = status

    def vars(self):
        d = vars(self)
        d['status'] = str(d['status']).removeprefix('Status.')
        return d


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
        saved = self.read(order.id)

        if order.status is None:
            order.status = saved.status

        self.orders[order.id] = order

        return order

    def read(self, id):
        id = int(id)
        try:
            return self.orders[id]
        except KeyError as e:
            raise DoesNotExist(id)