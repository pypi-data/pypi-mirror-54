'''objectmapper exception classes'''
class ObjectMapperError(Exception):
    '''Parent exception class'''


class DuplicateMappingError(ObjectMapperError):
    '''Raised when a mapping between classes is redundantly defined without forcing an overwrite.'''
    def __init__(self, input_type, output_type, mapping):
        super().__init__(f'Mapping already exists from {input_type} to {output_type} -- {mapping}')


class MapTypeError(ObjectMapperError, TypeError):
    '''Raised when attempting to create an invalid mapping.'''
    def __init__(self, invalid_type):
        super().__init__(f'{invalid_type} is not a valid type')


class MapFunctionTypeError(ObjectMapperError, TypeError):
    '''Raised when an a map function is not a callable'''
    def __init__(self, invalid_map_function):
        super().__init__(f'{invalid_map_function} is not callable')


class MapKeyError(ObjectMapperError, KeyError):
    '''Raised when a mapping is called, but not defined'''


class MapInputKeyError(MapKeyError):
    '''Raised when mapping an object of an unknown type.'''
    def __init__(self, input_type):
        super().__init__(f'No mappings found for instances of type {input_type}')


class MapOutputKeyError(MapKeyError):
    '''Raised when mapping an object to an unknown type.'''
    def __init__(self, input_type, output_type):
        super().__init__(f'No mappings found from instances of type {input_type} to type'
                         f' {output_type}')
