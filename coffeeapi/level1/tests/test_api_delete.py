from http import HTTPStatus


def test_delete_success(client, onecoffee):
    url = '/order/delete?id=1'
    response = client.post(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(onecoffee.orders) == 0


def test_delete_not_allowed(client, onecoffee):
    url = '/order/delete?id=1'
    response = client.get(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert len(onecoffee.orders) == 1


def test_delete_badreq(client, onecoffee):
    url = '/order/delete'
    response = client.post(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(onecoffee.orders) == 1


def test_delete_not_found(client, onecoffee):
    url = '/order/delete?id=404'
    response = client.post(url)

    assert response.status_code == HTTPStatus.NOT_FOUND