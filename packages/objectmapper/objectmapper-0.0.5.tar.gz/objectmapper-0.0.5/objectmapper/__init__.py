# pylint: disable=missing-module-docstring
from typing import Any, Callable, Optional, Type, TypeVar

from .objectmapper import ObjectMapper, _InputType, _OutputType
from .exceptions import (
    DuplicateMappingError,
    MapTypeError,
    MapFunctionTypeError,
    MapKeyError,
    MapInputKeyError,
    MapOutputKeyError,
    ObjectMapperError,
)


__all__ = [
    'create_map',
    'DuplicateMappingError',
    'map',
    'MapTypeError',
    'MapFunctionTypeError',
    'MapKeyError',
    'MapInputKeyError',
    'MapOutputKeyError',
    'ObjectMapper',
    'ObjectMapperError',
]


_OBJECT_MAPPER = ObjectMapper()


def create_map(input_type: Type[_InputType],
               output_type: Type[_OutputType],
               map_function: Callable[[_InputType], _OutputType] = None,
               force: bool = False) \
               -> Optional[Callable[[Callable[[_InputType], _OutputType]], None]]:
    '''Stores a mapping (`map_function`) from objects of type `input_type`
    to an object of type `output_type`. If `force` is `True`, then any
    pre-existing mapping from `input_type` to `output_type` is
    overwritten.

    .. testsetup:: create_map_explicit

       import objectmapper

    .. doctest:: create_map_explicit

       >>> objectmapper.create_map(int, str, lambda i: str(i))
       >>> objectmapper.map(42, str)
       '42'

    .. testcleanup:: create_map_explicit

       import importlib
       importlib.reload(objectmapper)

    Can also be used as a _decorator_

    .. testsetup:: create_map_decorator

       import objectmapper

    .. doctest:: create_map_decorator

       >>> @objectmapper.create_map(int, str)
       ... def int_to_str(i: int) -> str:
       ...     return str(i)
       >>> objectmapper.map(42, str)
       '42'

    .. testcleanup:: create_map_decorator

       import importlib
       importlib.reload(objectmapper)

    `MapTypeError` is raised if `input_type` or `output_type` are not
    types.

    `MapFunctionTypeError` is raised if `map_function` is not
    callable.

    `DuplicateMappingError` is raised if there is a pre-existing
    mapping from `input_type` to `output_type` and `force` is `False`.
    '''
    return _OBJECT_MAPPER.create_map(input_type, output_type, map_function, force)


def map(input_instance: Any, output_type: Type[_OutputType]) -> _OutputType:  # pylint: disable=redefined-builtin
    '''Returns an object of type `output_type` by giving `input_instance`
    to the mapping from `type(input_instance)` to `output_type`.

    .. testsetup:: map

       import objectmapper

    .. doctest:: map

       >>> import objectmapper
       >>> @objectmapper.create_map(int, str)
       ... def longform_int_to_str(i: int) -> str:
       ...     digits = (str(x) for x in range(10))
       ...     words = ['zero', 'one', 'two', 'three', 'four',
       ...              'five', 'six', 'seven', 'eight', 'nine']
       ...     digit_to_word = {d: w for d, w in zip(digits, words)}
       ...     return ' '.join(digit_to_word[c] for c in str(i))
       >>> objectmapper.map(451, str)
       'four five one'

    .. testcleanup:: map

       import importlib
       importlib.reload(objectmapper)


    Raises `MapInputKeyError` if there are no mappings from
    `type(input_instance)`.

    Raises `MapOutputKeyError` if there are no mappings from
    `type(input_instance)` to `output_type`.
    '''
    return _OBJECT_MAPPER.map(input_instance, output_type)
