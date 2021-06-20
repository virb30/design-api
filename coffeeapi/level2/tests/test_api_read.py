from datetime import datetime
from http import HTTPStatus

import pytest


def test_read_success(apiclient, onecoffee):
    url = '/order/1'
    response = apiclient.get(url)

    assert response.status_code == HTTPStatus.OK

    expected = dict(id=1, coffee='latte', size='large', milk='whole', location='takeAway',
                    created_at=datetime(2021, 4, 28), status='Placed')
    assert response.json() == expected


@pytest.mark.skip
def test_read_not_allowed(client, onecoffee):
    url = '/order/1'
    response = client.post(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.skip
def test_read_badreq(client, onecoffee):
    url = '/order'
    response = client.get(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_not_found(apiclient, onecoffee):
    url = '/order/404'
    response = apiclient.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND