from datetime import datetime
from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_update_success(apiclient, onecoffee):
    url = '/v3/order/1'
    data = dict(coffee='curto', milk='', size='small', location='takeAway')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(onecoffee.orders) == 1
    assert (dict(coffee='curto', milk='', size='small', id=1, location='takeAway',
                 created_at=datetime(2021, 4, 28), status='Placed',
                links=dict(
                    cancel=dict(url='/v3/order/1', method='DELETE'),
                    payment=dict(url='/v3/payment/1', method='PUT'),
                    receipt=None, self=dict(url='/v3/order/1', method='GET'),
                    update=dict(url='/v3/order/1', method='PUT')
                ))
            == onecoffee.read(1).vars())


def test_update_badreq(apiclient, onecoffee):
    url = '/v3/order/1'
    data = dict(coffee='curto', milk='', size='small')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(onecoffee.orders) == 1


def test_update_not_found(apiclient, onecoffee):
    url = '/v3/order/404'
    data = dict(coffee='curto', milk='', size='small', location='takeAway')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_conflict(apiclient, order, coffeeshop):
    url = '/v3/order/1'
    order.status = Status.Paid
    coffeeshop.create(order)
    data = dict(coffee='curto', milk='', size='small', location='takeAway')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.CONFLICT