from functools import partialmethod

from django.test import Client

from coffeeapi.level2.framework.http import DEFAULT_CT
# class APIClient(Client):
#     def post(self, *args, **kwargs):
#         kwargs['content_type'] = DEFAULT_CT
#         return super().post(*args, **kwargs)
#
#     def get(self, *args, **kwargs):
#         kwargs['content_type'] = DEFAULT_CT
#         return super().get(*args, **kwargs)
#
#     def put(self, *args, **kwargs):
#         kwargs['content_type'] = DEFAULT_CT
#         return super().put(*args, **kwargs)
#
#     def delete(self, *args, **kwargs):
#         kwargs['content_type'] = DEFAULT_CT
#         return super().delete(*args, **kwargs)
from coffeeapi.level2.framework.serializers import MyJSONEncoder, MyJSONDecoder

APIClient = type('APIClient',
                 (Client,),
                 {
                     '__init__': partialmethod(Client.__init__, json_encoder=MyJSONEncoder),
                     '_parse_json': partialmethod(Client._parse_json, cls=MyJSONDecoder),
                     **{verb: partialmethod(getattr(Client, verb), content_type=DEFAULT_CT)
                        for verb in ('post', 'get', 'put', 'delete')},
                 }
)