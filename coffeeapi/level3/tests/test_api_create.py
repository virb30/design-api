from datetime import datetime
from http import HTTPStatus

import pytest


def test_post_sucess(apiclient, coffeeshop):
    url = '/v3/order'
    data = dict(coffee='latte', size='large', milk='whole', location='takeAway')
    response = apiclient.post(url, data=data)
    created_time = datetime(2021, 4, 28)

    assert response.status_code == HTTPStatus.CREATED
    assert dict(id=1, coffee='latte', size='large', milk='whole',
                location='takeAway', status='Placed', created_at=created_time,
                links=dict(
                    cancel=dict(url='/v3/order/1', method='DELETE'),
                    payment=dict(url='/v3/payment/1', method='PUT'),
                    receipt=None,
                    self=dict(url='/v3/order/1', method='GET'),
                    update=dict(url='/v3/order/1', method='PUT')
                )) == coffeeshop.read(1).vars()
    assert len(coffeeshop.orders) == 1

    expected = dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                    created_at=datetime(2021, 4, 28), status='Placed',
                    links=dict(
                        cancel=dict(url='/v3/order/1', method='DELETE'),
                        payment=dict(url='/v3/payment/1', method='PUT'),
                        receipt=None, self=dict(url='/v3/order/1', method='GET'),
                        update=dict(url='/v3/order/1', method='PUT')
                    ))
    assert response.json() == expected


def test_post_badreq(apiclient, coffeeshop):
    url = '/v3/order'
    data = dict(coffee='latte', size='large', milk='whole')
    response = apiclient.post(url, data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(coffeeshop.orders) == 0