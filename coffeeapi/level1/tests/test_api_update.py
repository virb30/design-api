from http import HTTPStatus


def test_update_success(client, onecoffee):
    url = '/order/update?id=1&coffee=curto&milk=&size=small&location=takeAway'
    response = client.post(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(onecoffee.orders) == 1
    assert (dict(coffee='curto', milk='', size='small', id=1, location='takeAway')
            == vars(onecoffee.read(1)))


def test_update_not_allowed(client, onecoffee):
    url = '/order/update?id=1'
    response = client.get(url)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert len(onecoffee.orders) == 1


def test_update_badreq(client, onecoffee):
    url = '/order/update'
    response = client.post(url)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert len(onecoffee.orders) == 1


def test_update_not_found(client, onecoffee):
    url = '/order/update?id=404&coffee=curto&milk=&size=small&location=takeAway'
    response = client.post(url)

    assert response.status_code == HTTPStatus.NOT_FOUND