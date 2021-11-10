import re
import types
from functools import partial
from collections import defaultdict

from pipert2.core.base.data import Data


def class_functions_dictionary():
    """Create a decorator for marking functions and storing them in a
    dictionary by their class and their marking signature

    Returns:
        Decorator that stores its functions in the 'all' attribute.

    Example usage:

    >>> class Bakery:
    ...     cooking_styles = class_functions_dictionary()
    ...
    ...     @cooking_styles("indian")
    ...     def indian_backing(self):
    ...         pass
    ...
    ...     @cooking_styles("asian")
    ...     def asian_backing(self):
    ...         pass
    ...
    ...     @classmethod
    ...     def get_cooking_styles(cls):
    ...         return cls.cooking_styles.all(cls)


    >>> print(Bakery.get_cooking_styles())  # {'indian': [<function Bakery.indian_backing at 0x7f8c4f339dc0>],
    ...                                     #  'asian': [<function Bakery.asian_backing at 0x7f8c4f339e50>]})

    """

    registry = defaultdict(lambda: defaultdict(set))

    def key_registrar(keys_or_function):
        if callable(keys_or_function):
            # No key was given to the function, setting a defualt key
            return register(keys="default_key", function=keys_or_function)
        else:
            return partial(register, keys=keys_or_function)

    def register(function, keys):
        # Get the class name from the function __str__ attribute using regular expression
        class_name = re.search(' (.*)\\.', function.__str__()).group(1)

        keys = [keys] if not isinstance(keys, list) else keys

        for key in keys:
            registry[class_name][key].add(function)

        return function

    def get_functions(cls):
        if hasattr(cls, "__name__"):
            return registry[cls.__name__]
        else:
            return registry[cls]

    key_registrar.all = get_functions

    return key_registrar


def main_logics_dictionary():
    """Create a decorator for marking functions as main logics and storing them in a
    dictionary by their class and their expected input data type.

    Returns:
        Decorator that stores its functions in the 'all' attribute.

    Example usage:

    >>> class Bakery:
    ...     cooking_styles = class_functions_dictionary()
    ...
    ...     @cooking_styles("indian")
    ...     def indian_backing(self):
    ...         pass
    ...
    ...     @cooking_styles("asian")
    ...     def asian_backing(self):
    ...         pass
    ...
    ...     @classmethod
    ...     def get_cooking_styles(cls):
    ...         return cls.cooking_styles.all(cls)


    >>> print(Bakery.get_cooking_styles())  # {'indian': [<function Bakery.indian_backing at 0x7f8c4f339dc0>],
    ...                                     #  'asian': [<function Bakery.asian_backing at 0x7f8c4f339e50>]})

    """

    registry = defaultdict(dict)

    def key_registrar(expected_input_type):
        if isinstance(expected_input_type, types.FunctionType):
            return register(keys=Data, function=expected_input_type)
        else:
            return partial(register, keys=expected_input_type)

    def register(function, keys):
        # Get the class name from the function __str__ attribute using regular expression
        class_name = re.search(' (.*)\\.', function.__str__()).group(1)

        keys = [keys] if not isinstance(keys, list) else keys

        for key in keys:
            if class_name in registry and key in registry[class_name]:
                raise ReferenceError(f"The datatype {key} already have a main logic function in the {class_name} class")
            registry[class_name][key] = function

        return function

    def get_functions(cls):
        if hasattr(cls, "__name__"):
            return registry[cls.__name__]
        else:
            return registry[cls]

    key_registrar.all = get_functions

    return key_registrar
