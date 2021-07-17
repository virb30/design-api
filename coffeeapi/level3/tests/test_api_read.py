from datetime import datetime
from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_read_success(apiclient, onecoffee):
    url = '/v3/order/1'
    response = apiclient.get(url)

    assert response.status_code == HTTPStatus.OK

    links = dict(
        self='http://testserver/v3/order/1',
        update='http://testserver/v3/order/1',
        cancel='http://testserver/v3/order/1',
        payment='http://testserver/v3/payment/1'
    )

    expected = dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                    created_at=datetime(2021, 4, 28), status='Placed', links=links)
    assert response.json() == expected


def test_read_paid_links(apiclient, onecoffee):
    onecoffee.read(1).status = Status.Paid
    url = '/v3/order/1'
    response = apiclient.get(url)

    assert response.json()['links'] == dict(self='http://testserver/v3/order/1')


def test_read_served_links(apiclient, onecoffee):
    onecoffee.read(1).status = Status.Served
    url = '/v3/order/1'
    response = apiclient.get(url)

    links = dict(
        self='http://testserver/v3/order/1',
        receipt='http://testserver/v3/receipt/1'
    )

    assert response.json()['links'] == links


def test_read_not_found(apiclient, onecoffee):
    url = '/v3/order/404'
    response = apiclient.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND