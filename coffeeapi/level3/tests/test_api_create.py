from datetime import datetime
from http import HTTPStatus

import pytest


def test_post_sucess(apiclient, coffeeshop):
    url = '/v3/order'
    data = dict(coffee='latte', size='large', milk='whole', location='takeAway')
    response = apiclient.post(url, data=data)
    created_time = datetime(2021, 4, 28)

    assert response.status_code == HTTPStatus.CREATED
    assert response.headers['location'] == 'http://testserver/v3/order/1'
    assert len(coffeeshop.orders) == 1

    links = dict(
        self='http://testserver/v3/order/1',
        update='http://testserver/v3/order/1',
        cancel='http://testserver/v3/order/1',
        payment='http://testserver/v3/payment/1'
    )

    # links = [
    #     {
    #         'rel': 'self',
    #         'src': 'http://testserver/order/1',
    #         'verb': 'GET',
    #     },
    #     {
    #         'rel': 'update',
    #         'src': 'http://testserver/order/1',
    #         'verb': 'PUT',
    #     },
    #     {
    #         'rel': 'cancel',
    #         'src': 'http://testserver/order/1',
    #         'verb': 'DELETE',
    #     },
    #     {
    #         'rel': 'payment',
    #         'src': 'http://testserver/payment/1',
    #         'verb': 'PUT',
    #     },
    # ]

    expected = dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                    created_at=datetime(2021, 4, 28), status='Placed', links=links)
    assert response.json() == expected


def test_post_badreq(apiclient, coffeeshop):
    url = '/v3/order'
    data = dict(coffee='latte', size='large', milk='whole')
    response = apiclient.post(url, data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(coffeeshop.orders) == 0