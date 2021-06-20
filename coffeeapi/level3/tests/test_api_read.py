from datetime import datetime
from http import HTTPStatus

import pytest


def test_read_success(apiclient, onecoffee):
    url = '/v3/order/1'
    response = apiclient.get(url)

    assert response.status_code == HTTPStatus.OK

    expected = dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                    created_at=datetime(2021, 4, 28), status='Placed',
                    links=dict(
                        cancel=dict(url='/v3/order/1', method='DELETE'),
                        payment=dict(url='/v3/payment/1', method='PUT'),
                        receipt=None, self=dict(url='/v3/order/1', method='GET'),
                        update=dict(url='/v3/order/1', method='PUT')
                    ))
    assert response.json() == expected



def test_read_not_found(apiclient, onecoffee):
    url = '/v3/order/404'
    response = apiclient.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND