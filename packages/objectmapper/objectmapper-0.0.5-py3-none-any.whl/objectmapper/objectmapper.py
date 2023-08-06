'''ObjectMapper Class'''

from typing import Any, Callable, Optional, Type, TypeVar

from . import exceptions


_InputType = TypeVar('_InputType')
_OutputType = TypeVar('_OutputType')


class ObjectMapper:
    '''Class for recording and accessing mappings between object
    types. This will often be a singleton in user code.

    '''
    def __init__(self) -> None:
        self._mappings = dict()

    def create_map(self,
                   input_type: Type[_InputType],
                   output_type: Type[_OutputType],
                   map_function: Optional[Callable[[_InputType], _OutputType]] = None,
                   force: bool = False) \
                   -> Optional[Callable[[Callable[[_InputType], _OutputType]], None]]:
        '''Stores a localized mapping between types. See `create_map`'''
        for map_type in [input_type, output_type]:
            if not isinstance(map_type, type):
                raise exceptions.MapTypeError(map_type)

        def set_map_function(map_function: Callable[[_InputType], _OutputType]) -> None:
            if not callable(map_function):
                raise exceptions.MapFunctionTypeError(map_function)

            self._mappings.setdefault(input_type, dict())

            if not force:
                mapping = self._mappings[input_type].get(output_type, None)
                if mapping:
                    raise exceptions.DuplicateMappingError(input_type, output_type, mapping)
            self._mappings[input_type][output_type] = map_function

        if map_function is None:
            return set_map_function
        return set_map_function(map_function)

    def map(self, input_instance: Any, output_type: Type[_OutputType]) -> _OutputType:
        '''Converts `input_instance` using a mapping from
        `type(input_instance)` to `output_type`. See `map`.

        '''
        input_type = type(input_instance)
        if input_type not in self._mappings:
            raise exceptions.MapInputKeyError(input_type)

        map_function = self._mappings[input_type].get(output_type, None)
        if not map_function:
            raise exceptions.MapOutputKeyError(input_type, output_type)

        return map_function(input_instance)
