import functools
import json

from django.utils.datastructures import MultiValueDictKeyError

from coffeeapi.level2.framework.http import MethodNotAllowed, BadRequest


class allow:
    def __init__(self, *methods):
        self.allowed = tuple(m.upper() for m in methods)

    def __call__(self, view):
        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.method not in self.allowed:
                return MethodNotAllowed()

            return view(request, *args, **kwargs)

        return wrapper


class require:
    def __init__(self, *params):
        self.params = tuple(params)

    def __call__(self, view):
        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            try:
                params = {k: request.GET[k] for k in self.params}
            except MultiValueDictKeyError as e:
                return BadRequest(str(e).strip("'"))

            kwargs['params'] = params

            return view(request, *args, **kwargs)
        return wrapper


class datarequired:
    def __init__(self, *params):
        self.params = tuple(params)

    def __call__(self, view):
        @functools.wraps(view)
        def wrapper(request, *args, **kwargs):
            try:
                params = json.loads(request.body)
                assert all(p in params for p in self.params)
            except AssertionError as e:
                return BadRequest('Bad request.')

            kwargs['params'] = params

            return view(request, *args, **kwargs)
        return wrapper
