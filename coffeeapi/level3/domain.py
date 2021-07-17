from decimal import Decimal
from enum import Enum, auto


def now():
    from django.utils.datetime_safe import datetime
    return datetime.now()


class Status(Enum):
    Placed = auto()     # Pedido / Aguardando Pagamento
    Paid = auto()   # Pago
    Served = auto()   # Pronto
    Collected = auto()  # Entregue
    Cancelled = auto()   # Cancelado


class Link:
    def __init__(self, url, method='GET'):
        self.url = url
        self.method = method


O_PATRAO_ESTA_MALUCO = Decimal('1.99')


class Order:
    def __init__(self, coffee='', size='', milk='', location='', id=None, created_at=None, status=None):
        self.id = None if id is None else int(id)
        self.coffee = coffee
        self.size = size
        self.milk = milk
        self.location = location
        self.created_at = now() if created_at is None else created_at
        self.status = status
        self.price = O_PATRAO_ESTA_MALUCO

    def vars(self):
        d = vars(self).copy()
        d['status'] = str(d['status']).removeprefix('Status.')
        # TODO: Atualizar a desserialização do price
        del d['price']
        return d

    def is_cancelled(self):
        return self.status == Status.Cancelled

    def is_paid(self):
        return self.status == Status.Paid

    def is_collected(self):
        return self.status == Status.Collected

    def is_served(self):
        return self.status == Status.Served

    def is_placed(self):
        return self.status == Status.Placed


class DoesNotExist(Exception):
    pass


class Conflicted(Exception):
    pass


class CoffeeShop:
    def __init__(self):
        self.orders = {}

    def create(self, order):
        if order.id is None:
            order.id = len(self.orders) + 1
        self.orders[order.id] = order
        return order

    def delete(self, id):
        # TODO: parece igual ao read
        order = self.read(id)

        if order.status != Status.Placed:
            raise Conflicted()

        order.status = Status.Cancelled
        return order

    def update(self, order):
        saved = self.read(order.id)

        if saved.status != Status.Placed:
            raise Conflicted()

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

    def pay(self, id):
        order = self.read(id)

        if order.status != Status.Placed:
            raise Conflicted()

        order.status = Status.Paid

        return order

    def pay(self, id, amount):
        # TODO: mover para deserialize
        amount = Decimal(amount) / 100
        order = self.read(id)

        if order.is_paid():
            raise Conflicted(id)

        if amount == order.price:
            order.status = Status.Paid
        return order

    def deliver(self, id):
        order = self.read(id)

        if order.is_collected():
            raise Conflicted()

        order.status = Status.Collected
        return order
