import copy
from typing import ClassVar, Dict, Optional, Callable

from .attribute import Attribute


class E(Exception):
    """Error Object"""

    __id = 0
    sid2e = dict()  # type: Dict[str, E]
    eid2e = dict()  # type: Dict[int, E]

    """
    Old version has an attribute "ph", which means the placeholder style.
    Now we standardize it as "format".
    """

    def __init__(self, message: str):
        self.message = message  # str
        self.debug_message = None
        self.eid = E.__id
        self.class_ = None  # type: ClassVar

        self.as_template = True
        self.origin = self
        self._identifier = None

        E.__id += 1

    def d(self):
        return Attribute.dictify(self, 'message->msg', 'eid')

    def d_debug(self):
        return Attribute.dictify(self, 'message->msg', 'eid', 'debug_message', 'identifier')

    def eis(self, e: 'E'):
        return self.eid == e.eid

    @property
    def ok(self):
        return self.eid == BaseError.OK.eid

    def _instantiate(self, *args, debug_message: str = None, **kwargs):
        instance = copy.copy(self.origin)

        instance.as_template = False
        instance.debug_message = debug_message
        try:
            instance.message = instance.message.format(*args, **kwargs)
        except Exception as err:
            raise BaseError.ERROR_GENERATE(debug_message=err)
        return instance

    def __call__(self, *args, debug_message=None, **kwargs):
        if debug_message and not isinstance(debug_message, str):
            debug_message = str(debug_message)
        return self._instantiate(*args, debug_message=debug_message, **kwargs)

    def __str__(self):
        return 'Id: %s, Message: %s' % (self.eid, self.message)

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        if self.identifier is not None:
            raise RuntimeError('Error %s already has the identifier "%s"' % (
                str(self), self.identifier))
        self._identifier = value

    @classmethod
    def register(cls, id_processor: Optional[Callable] = None):
        def wrapper(class_: ClassVar):
            for name in class_.__dict__:  # type: str
                e = getattr(class_, name)
                if isinstance(e, E) and e.as_template:
                    if callable(id_processor):
                        identifier = id_processor(name, class_)
                    else:
                        identifier = name
                    if identifier in cls.sid2e:
                        raise AttributeError(
                            'Conflict error identifier({0}), within class {1} and class {2}'.format(
                                identifier, cls.sid2e[identifier].class_.__name__, class_.__name__))

                    e.identifier = identifier
                    e.class_ = class_
                    cls.sid2e[identifier] = e
                    cls.eid2e[e.eid] = e
            return class_
        return wrapper

    @classmethod
    def all(cls):
        dict_ = dict()
        for k, v in cls.sid2e.items():
            dict_[k] = v.d()
        return dict_


@E.register()
class BaseError:
    OK = E("OK")
    ERROR_GENERATE = E("Something goes wrong when generating an error.")
