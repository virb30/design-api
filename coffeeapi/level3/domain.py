from enum import Enum, auto


def now():
    from django.utils.datetime_safe import datetime
    return datetime.now()


class Status(Enum):
    Placed = auto()     # Pedido / Aguardando Pagamento
    Paid = auto()   # Pago
    Done = auto()   # Pronto
    Collected = auto()  # Entregue
    Canceled = auto()   # Cancelado


class Link:
    def __init__(self, url, method='GET'):
        self.url = url
        self.method = method


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
        d['links'] = {
            'self':  vars(Link(f'/v3/order/{self.id}', 'GET')),
            'update': vars(Link(f'/v3/order/{self.id}', 'PUT')) if self.status == Status.Placed.name else None,
            'cancel': vars(Link(f'/v3/order/{self.id}', 'DELETE')) if self.status == Status.Placed.name else None,
            'payment': vars(Link(f'/v3/payment/{self.id}', 'PUT')) if self.status == Status.Placed.name else None,
            'receipt': vars(Link(f'/v3/receipt/{self.id}', 'DELETE')) if self.status == Status.Paid.name else None
        }
        return d


class DoesNotExist(Exception):
    pass


class StatusConflict(Exception):
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
        saved = self.read(order.id)

        if saved.status != Status.Placed:
            raise StatusConflict()

        saved.status = Status.Canceled

    def update(self, order):
        saved = self.read(order.id)

        if saved.status != Status.Placed:
            raise StatusConflict()

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
            raise StatusConflict()

        order.status = Status.Paid

        return order

    def receipt(self, id):
        order = self.read(id)

        if order.status != Status.Done:
            raise StatusConflict()

        order.status = Status.Collected
        return order
