import functools
from http import HTTPStatus

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from coffeeapi.level1.domain import DoesNotExist

DEFAULT_CT = 'text/plain; charset=utf-8'

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


class allow:
    def __init__(self, *methods):
        self.allowed = tuple(m.upper() for m in methods)

    def __call__(self, view):
        @functools.wraps(view)
        def wrapper(request):
            if request.method not in self.allowed:
                return MethodNotAllowed()

            return view(request)

        return wrapper


class require:
    def __init__(self, *params):
        self.params = tuple(params)

    def __call__(self, view):
        @functools.wraps(view)
        def wrapper(request):
            try:
                params = {k: request.GET[k] for k in self.params}
            except MultiValueDictKeyError as e:
                return BadRequest(str(e).strip("'"))

            return view(request, params)
        return wrapper


class FrameworkCommonExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exc):
        if isinstance(exc, DoesNotExist):
            return NotFound()


def serialize(obj):
    return '\n'.join((f'{k}={v}' for k, v in sorted(vars(obj).items())))
