from coopy.base import init_persistent_system

from coffeeapi.level2.domain import CoffeeShop, Order, Status
from coffeeapi.level2.framework import Created, NoContent, allow, serialize, Ok, datarequired, abs_reverse

coffeeshop = init_persistent_system(CoffeeShop(), basedir='data/level2')

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

    return Created(
        serialize(order),
        headers={'Location': abs_reverse(request, 'order', args=(order.id,))}
    )


@allow('DELETE')
def delete(request, id):
    order = Order(id=id)
    order = coffeeshop.delete(order)

    return NoContent()


@allow('PUT')
@datarequired('coffee', 'size', 'milk', 'location')
def update(request, id, params=None):
    order = Order(id=id, **params)
    order = coffeeshop.update(order)

    return NoContent()


@allow('GET')
def read(request, id):
    order = coffeeshop.read(id)

    return Ok(serialize(order))