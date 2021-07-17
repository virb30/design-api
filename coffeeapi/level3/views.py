from decimal import Decimal

from coopy.base import init_persistent_system

from coffeeapi.level3.domain import CoffeeShop, Order, Status
from coffeeapi.level3.framework import Created, NoContent, allow, serialize, Ok, datarequired, abs_reverse

coffeeshop = init_persistent_system(CoffeeShop(), basedir='data/level3')


def order_links(request, order):
    link_to_self = abs_reverse(request, 'orderv3', args=(order.id,))

    links = {}
    if order.is_placed():
        links.update(
            self=link_to_self,
            update=link_to_self,
            cancel=link_to_self,
            payment=abs_reverse(request, 'payment', args=(order.id,))
        )
    elif order.is_paid():
       links.update(
            self=link_to_self,
        )
    elif order.is_served():
       links.update(
            self=link_to_self,
            receipt=abs_reverse(request, 'receipt', args=(order.id,))
        )

    return links


@allow('GET', 'POST', 'PUT', 'DELETE')
def dispatch(request, *args, **kwargs):
    methods = dict(GET=read, POST=create, PUT=update, DELETE=delete)
    view = methods[request.method]

    return view(request, *args, **kwargs)


@allow('POST')
@datarequired('coffee', 'size', 'milk', 'location')
def create(request, params=None):
    order = Order(**params, status=Status.Placed)
    coffeeshop.create(order)

    d = order.vars()
    d['links'] = order_links(request, order)

    return Created(
        serialize(d),
        headers={'Location': abs_reverse(request, 'orderv3', args=(order.id,))}
    )


@allow('DELETE')
def delete(request, id):
    order = coffeeshop.delete(id)
    return NoContent()


@allow('PUT')
@datarequired('coffee', 'size', 'milk', 'location')
def update(request, id, params=None):
    order = Order(id=id, **params)
    order = coffeeshop.update(order)

    d = order.vars()
    d['links'] = order_links(request, order)

    return Ok(
        serialize(d)
    )

@allow('GET')
def read(request, id):
    order = coffeeshop.read(id)

    d = order.vars()
    d['links'] = order_links(request, order)

    return Ok(serialize(d))


@allow('PUT')
@datarequired('amount')
def payment(request, id, params=None):
    order = coffeeshop.pay(id, **params)

    d = {'links': order_links(request, order)}

    return Ok(serialize(d))


@allow('DELETE')
def receipt(request, id):
    coffeeshop.deliver(id=id)
    return NoContent()
