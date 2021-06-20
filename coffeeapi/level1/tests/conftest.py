import pytest

from coffeeapi.level1.domain import CoffeeShop, Order


@pytest.fixture
def coffeeshop(mocker):
    cs = CoffeeShop()
    mocker.patch('coffeeapi.level1.views.coffeeshop', cs)
    return cs


@pytest.fixture
def order():
    return Order(coffee='latte', size='large', milk='whole', location='takeAway')


@pytest.fixture
def onecoffee(coffeeshop, order):
    coffeeshop.create(order)
    return coffeeshop