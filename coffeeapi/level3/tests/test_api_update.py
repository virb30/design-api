from datetime import datetime
from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_update_success(apiclient, onecoffee):
    url = '/v3/order/1'
    data = dict(coffee='curto', milk='', size='small', location='takeAway')
    response = apiclient.put(url, data=data)

    links = dict(
        self='http://testserver/v3/order/1',
        update='http://testserver/v3/order/1',
        cancel='http://testserver/v3/order/1',
        payment='http://testserver/v3/payment/1'
    )

    expected = dict(
        coffee='curto', milk='', size='small', id=1, location='takeAway',
        created_at=datetime(2021, 4, 28), status='Placed', links=links)

    assert response.status_code == HTTPStatus.OK
    assert len(onecoffee.orders) == 1
    assert response.json() == expected


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