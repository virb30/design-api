import abc
import json
from datetime import datetime
from json import JSONDecoder

from django.core.serializers.json import DjangoJSONEncoder


# def serialize(obj):
#     return '\n'.join((f'{k}={v}' for k, v in sorted(vars(obj).items())))

def serialize(obj):
    return json.dumps(obj, cls=MyJSONEncoder)

def deserialize(s):
    return json.loads(s, cls=MyJSONDecoder)


class IMySerializable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, 'vars') and
            callable(subclass.vars)
        )

    @abc.abstractmethod
    def vars(self):
        pass
    

class MyJSONEncoder(DjangoJSONEncoder):
    def encode(self, o):
        if isinstance(o, IMySerializable):
            o = o.vars()
        return super().encode(o)


class MyJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.hook, *args, **kwargs)

    @staticmethod
    def hook(source):
        d = {}
        for k, v in source.items():
            if isinstance(v, str) and not v.isdigit():
                try:
                    d[k] = datetime.fromisoformat(v)
                except (ValueError, TypeError):
                    d[k] = v
            else:
                d[k] = v

        return d
