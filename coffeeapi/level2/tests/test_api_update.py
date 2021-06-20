from datetime import datetime
from http import HTTPStatus

import pytest


def test_update_success(apiclient, onecoffee):
    url = '/order/1'
    data = dict(coffee='curto', milk='', size='small', location='takeAway')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(onecoffee.orders) == 1
    assert (dict(coffee='curto', milk='', size='small', id=1, location='takeAway',
                 created_at=datetime(2021, 4, 28), status='Placed')
            == onecoffee.read(1).vars())


@pytest.mark.skip
def test_update_not_allowed(client, onecoffee):
    url = '/order?id=1'
    response = client.get(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert len(onecoffee.orders) == 1


def test_update_badreq(apiclient, onecoffee):
    url = '/order/1'
    data = dict(coffee='curto', milk='', size='small')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(onecoffee.orders) == 1


def test_update_not_found(apiclient, onecoffee):
    url = '/order/404&coffee=curto&milk=&size=small&location=takeAway'
    data = dict(coffee='curto', milk='', size='small', location='takeAway')
    response = apiclient.put(url, data=data)

    assert response.status_code == HTTPStatus.NOT_FOUND