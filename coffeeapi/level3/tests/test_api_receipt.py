from datetime import datetime
from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_receipt_success(apiclient, order, coffeeshop):
    url = '/v3/receipt/1'
    order.status = Status.Done
    coffeeshop.create(order)
    response = apiclient.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_receipt_method_not_allowed(apiclient, onecoffee):
    url = '/v3/receipt/1'
    response = apiclient.post(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_receipt_conflict(apiclient, order, coffeeshop):
    url = '/v3/receipt/1'
    order.status = Status.Paid
    coffeeshop.create(order)
    response = apiclient.delete(url)

    assert response.status_code == HTTPStatus.CONFLICT


def test_receipt_not_found(apiclient, onecoffee):
    url = '/v3/receipt/404'
    response = apiclient.delete(url)

    assert response.status_code == HTTPStatus.NOT_FOUND