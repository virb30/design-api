from http import HTTPStatus

import pytest

from coffeeapi.level3.domain import Status


def test_delete_success(apiclient, onecoffee):
    url = '/v3/order/1'
    response = apiclient.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(onecoffee.orders) == 1
    assert onecoffee.read(1).is_cancelled()


def test_delete_not_found(apiclient, onecoffee):
    url = '/v3/order/404'
    response = apiclient.delete(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_conflict(apiclient, onecoffee):
    url = '/v3/order/1'
    onecoffee.read(1).status = Status.Paid
    response = apiclient.delete(url)

    assert response.status_code == HTTPStatus.CONFLICT