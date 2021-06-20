from http import HTTPStatus

from django.http import HttpResponse

DEFAULT_CT = 'application/json'

class MyResponse(HttpResponse):
    def __init__(self, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        if 'Content-Type' not in headers:
            headers['Content-Type'] = DEFAULT_CT

        super(MyResponse, self).__init__(*args, **kwargs)


class MethodNotAllowed(MyResponse):
    status_code = HTTPStatus.METHOD_NOT_ALLOWED

    def __init__(self, *args, **kwargs):
        super(MethodNotAllowed, self).__init__(
            HTTPStatus.METHOD_NOT_ALLOWED.description,
            *args, **kwargs
        )

class BadRequest(MyResponse):
    status_code = HTTPStatus.BAD_REQUEST


class Created(MyResponse):
    status_code = HTTPStatus.CREATED


class NotFound(MyResponse):
    status_code = HTTPStatus.NOT_FOUND


class NoContent(MyResponse):
    status_code = HTTPStatus.NO_CONTENT

class Ok(MyResponse):
    pass
