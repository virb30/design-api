from coopy.base import init_persistent_system

from coffeeapi.level1.domain import CoffeeShop, Order, DoesNotExist
from coffeeapi.level1.framework import Created, NoContent, allow, require, serialize, Ok, NotFound

coffeeshop = init_persistent_system(CoffeeShop(), basedir='data/level1')


@allow('POST')
@require('coffee', 'size', 'milk', 'location')
def create(request, params=None):
    order = Order(**params)
    coffeeshop.create(order)

    return Created(serialize(order))


@allow('POST')
@require('id')
def delete(request, params=None):
    order = Order(**params)
    coffeeshop.delete(order)
    return NoContent()


@allow('POST')
@require('id', 'coffee', 'size', 'milk', 'location')
def update(request, params=None):
    order = Order(**params)
    coffeeshop.update(order)

    return NoContent()


@allow('GET')
@require('id')
def read(request, params=None):
    order = coffeeshop.read(**params)
    return Ok(serialize(order))