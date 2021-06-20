from datetime import datetime
from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_payment_success(apiclient, onecoffee):
    url = '/v3/payment/1'
    response = apiclient.put(url)

    assert response.status_code == HTTPStatus.OK
    assert dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                created_at=datetime(2021, 4, 28), status='Paid',
                links=dict(
                    cancel=None,
                    payment=None,
                    receipt=dict(url='/v3/receipt/1', method='DELETE'),
                    self=dict(url='/v3/order/1', method='GET'),
                    update=None
                )) == onecoffee.read(1).vars()

    expected = dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                    created_at=datetime(2021, 4, 28), status='Paid',
                    links=dict(
                        cancel=None,
                        payment=None,
                        receipt=dict(url='/v3/receipt/1', method='DELETE'),
                        self=dict(url='/v3/order/1', method='GET'),
                        update=None
                    ))
    assert response.json() == expected


def test_payment_method_not_allowed(apiclient, onecoffee):
    url = '/v3/payment/1'
    response = apiclient.post(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_payment_conflict(apiclient, order, coffeeshop):
    url = '/v3/payment/1'
    order.status = Status.Paid
    coffeeshop.create(order)
    response = apiclient.put(url)

    assert response.status_code == HTTPStatus.CONFLICT


def test_payment_not_found(apiclient, onecoffee):
    url = '/v3/payment/404'
    response = apiclient.put(url)

    assert response.status_code == HTTPStatus.NOT_FOUND