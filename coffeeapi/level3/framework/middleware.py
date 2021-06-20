from coffeeapi.level3.domain import DoesNotExist, StatusConflict
from coffeeapi.level3.framework.http import NotFound, Conflict


class FrameworkCommonExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exc):
        if isinstance(exc, DoesNotExist):
            return NotFound()
        if isinstance(exc, StatusConflict):
            return Conflict()
