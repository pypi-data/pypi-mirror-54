import copy
import re
from typing import Union, Callable, Optional, List

from .attribute import Attribute
from .http_code import HttpCode as Hc
from .error import E
from .symbol import Symbol


@E.register()
class PError:
    PATTERN_NOT_MATCH = E("Pattern not match", hc=Hc.Forbidden)
    NULL_NOT_ALLOW = E("Param {0}({1}) is not allowed null", hc=Hc.Forbidden)
    REQUIRE_LIST = E("Param {0}({1}) should be a list", hc=Hc.Forbidden)
    REQUIRE_DICT = E("Param {0}({1}) should be a dict", hc=Hc.Forbidden)
    VALIDATOR_CRUSHED = E("Validator for {0}({1}) crushed", hc=Hc.InternalServerError)
    PROCESSOR_CRUSHED = E("Processor for {0}({1}) crushed", hc=Hc.InternalServerError)


class Processor:
    _DocWriters = {
        str: 'Convert type to string',
        int: 'Convert type to integer',
        float: 'Convert type to float',
        bool: 'Convert type to boolean',
    }

    @classmethod
    def doc_register(cls, writers):
        cls._DocWriters.update(writers)

    @classmethod
    def re_searcher(cls, pattern):
        def wrapper(value):
            """Extract/Validate information using RegExp"""

            result = re.search(pattern, value, flags=re.S)
            if result is None:
                raise PError.PATTERN_NOT_MATCH
            return result
        return wrapper

    def __init__(self,
                 processor: Union[Callable, str],
                 only_validate: bool = False,
                 yield_name: Optional[str] = None,
                 doc: Optional[str] = None):
        """
        A processor is a method or string, to process current value to what we want.
        :param processor: method or re string
        :param only_validate: as a validator
        :param yield_name: new variable name
        :param doc: description for this processor
        """
        self.processor = processor \
            if callable(processor) else self.re_searcher(pattern=processor)
        self.only_validate = only_validate
        self.yield_name = yield_name

        self.doc = doc or self._get_doc(processor)
        self.doc = self.doc or ('Validator' if only_validate else 'Processor')

    def _get_doc(self, processor):
        writer = self._DocWriters.get(processor)
        if writer:
            if isinstance(writer, str):
                return writer
            if callable(writer):
                return writer(processor)
        return processor.__doc__


class P:
    """Param Object for parameter validating and processing"""

    __NoDefault = Symbol()

    ATOM = Symbol()
    LIST = Symbol()
    DICT = Symbol()

    def __init__(self, name: str = None,
                 read_name: str = None,
                 yield_name: str = None,
                 type_: Symbol = ATOM):

        yield_name_, name = Attribute.arrow_extract(name)

        self.name = name
        self.read_name = read_name or name
        self.yield_name = yield_name or yield_name_

        self._null = False
        self._default_value = self.__NoDefault
        self._default_through_processors = False

        self._type = type_
        self._dict_fields = list()  # type: List[P]
        self._list_child = None  # type: Optional[P]

        self._processors = []

    def __str__(self):
        return '%s(%s)' % (self.name, self.read_name)

    @property
    def is_list(self):
        return self._type == self.LIST

    @property
    def is_dict(self):
        return self._type == self.DICT

    @property
    def is_atom(self):
        return self._type == self.ATOM

    def _set_dict_fields(self, *fields):
        self._dict_fields = list()
        return self._add_dict_fields(*fields)

    def _add_dict_fields(self, *fields: 'P'):
        self._dict_fields.extend(fields)
        return self

    def _set_list_child(self, child: Optional['P']):
        self._list_child = child
        return self

    def rename(self, name: str, read_name: str = None, yield_name: str = None, stay_origin=False):
        self.name = name
        self.read_name = read_name or (self.read_name if stay_origin else name)
        self.yield_name = yield_name or (self.yield_name if stay_origin else name)
        return self

    def null(self, allow=True):
        self._null = allow
        return self

    def default(self, value=None, allow=True, through_processors=False):
        if allow:
            self._default_value = value
        else:
            self._default_value = self.__NoDefault
        self._default_through_processors = through_processors
        return self

    def process(self, processor: Union[Processor, Callable], begin=False):
        if not isinstance(processor, Processor):
            processor = Processor(processor)
        if begin:
            self._processors.insert(0, processor)
        else:
            self._processors.append(processor)
        return self

    def validate(self, validator: Callable, begin=False):
        if begin:
            self._processors.insert(0, Processor(validator, only_validate=True))
        else:
            self._processors.append(Processor(validator, only_validate=True))
        return self

    def clone(self):
        p = copy.copy(self)
        p._processors = copy.copy(self._processors)
        p._dict_fields = copy.copy(self._dict_fields)
        return p

    @property
    def _has_default(self):
        return self._default_value != self.__NoDefault

    def run(self, value):
        yield_name = self.yield_name

        if value is None:
            if self._null:
                return yield_name, None
            if self._has_default:
                if not self._default_through_processors:
                    return yield_name, self._default_value
                else:
                    value = self._default_value
            else:
                raise PError.NULL_NOT_ALLOW(self.name, self.read_name)

        if self.is_list:
            if not isinstance(value, list):
                raise PError.REQUIRE_LIST(self.name, self.read_name)
            if isinstance(self._list_child, P):
                new_value = []
                for child_value in value:
                    _, child_new_value = self._list_child.run(child_value)
                    new_value.append(child_new_value)
                value = new_value
        elif self.is_dict:
            if not isinstance(value, dict):
                raise PError.REQUIRE_DICT(self.name, self.read_name)
            new_value = {}
            for child_field in self._dict_fields:
                child_value = value.get(child_field.name)
                child_yield_name, child_new_value = child_field.run(child_value)
                new_value[child_yield_name] = child_new_value
            value = new_value

        for processor in self._processors:
            error = PError.VALIDATOR_CRUSHED \
                if processor.only_validate else PError.PROCESSOR_CRUSHED

            try:
                result = processor.processor(value)
            except Exception as e:
                if isinstance(e, E):
                    raise e
                else:
                    raise error(self.name, self.read_name, debug_message=str(e))

            if not processor.only_validate:
                yield_name = processor.yield_name or yield_name
                value = result

        return yield_name, value


class PDict(P):
    def __init__(self, **kwargs):
        super(PDict, self).__init__(type_=P.DICT, **kwargs)

    def set_fields(self, *fields):
        return self._set_dict_fields(*fields)

    def add_fields(self, *fields):
        return self._add_dict_fields(*fields)


class PList(P):
    def __init__(self, **kwargs):
        super(PList, self).__init__(type_=P.LIST, **kwargs)

    def set_child(self, child=None):
        self._set_list_child(child=child)
        return self
