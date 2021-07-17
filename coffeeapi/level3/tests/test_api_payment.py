from datetime import datetime
from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_payment_success(apiclient, onecoffee):
    url = '/v3/payment/1'
    data = dict(amount=199)
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.OK

    links = dict(self='http://testserver/v3/order/1')
    expected = dict(links=links)
    assert response.json() == expected
    assert len(onecoffee.orders) == 1
    assert onecoffee.read(1).is_paid()


def test_payment_method_not_allowed(apiclient, onecoffee):
    url = '/v3/payment/1'
    response = apiclient.post(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_payment_not_found(apiclient, onecoffee):
    url = '/v3/payment/404'
    data = dict(amount='199')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_badreq(apiclient, onecoffee):
    url = '/v3/payment/1'
    data = dict()
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(onecoffee.orders) == 1
    assert not onecoffee.read(1).is_paid()


def test_payment_already_paid(apiclient, onecoffee):
    onecoffee.read(1).status = Status.Paid
    url = '/v3/payment/1'
    data = dict(amount=199)

    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.CONFLICT