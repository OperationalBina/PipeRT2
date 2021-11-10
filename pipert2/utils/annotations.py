import re
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
            return registrar(keys="default_key", function=keys_or_function)
        else:
            return partial(registrar, keys=keys_or_function)

    def registrar(function, keys):
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

    def key_registrar(keys_or_function):
        if callable(keys_or_function):
            # No key was given to the function, setting a defualt key
            return registrar(keys=Data, function=keys_or_function)
        else:
            return partial(registrar, keys=keys_or_function)

    def registrar(function, keys):
        # Get the class name from the function __str__ attribute using regular expression
        class_name = re.search(' (.*)\\.', function.__str__()).group(1)

        keys = [keys] if not isinstance(keys, list) else keys

        for key in keys:
            if class_name in registry and key in registry[class_name]:
                raise ReferenceError(f"The datatype {key} already have a main logic function")
                pass
            registry[class_name][key] = function

        return function

    def get_functions(cls):
        if hasattr(cls, "__name__"):
            return registry[cls.__name__]
        else:
            return registry[cls]

    key_registrar.all = get_functions

    return key_registrar

# main_logics = class_functions_dictionary()

#
# class Bakery(metaclass=MainLogicValidation, routines_registry=main_logics, validate_main_logic=False):
#     main_logics = main_logics
#
#     @main_logics("indian")
#     def indian_backing(self):
#         pass
#
#     @main_logics("asian")
#     def asian_backing(self):
#         pass
#
#     @classmethod
#     def get_main_logics(cls):
#         print(cls.__base__)
#         return cls.main_logics.all(cls)
#
#
# def stam(func):
#     print(f"Calling stam on {func}")
#     print(func)
#     print(getfullargspec(func))
#
#
# class OtherBakery(Bakery, metaclass=MainLogicValidation, validate_main_logic=stam):
#     pass
#
#
# class SonOtherBakery(OtherBakery):
#
#     @OtherBakery.main_logics("israel")
#     def israeli_backing(self, data: str) -> int:
#         pass
#
#
# class SonSonOtherBakery(SonOtherBakery):
#
#     @SonOtherBakery.main_logics("china")
#     def chinese_backing(self, data: int) -> tuple:
#         pass
#
#     # print(Bakery.get_cooking_styles())
#     # func = OtherBakery.get_cooking_styles()["israel"].pop()
#     # stam.
#     # print(func)
#     # print(func.__dict__)
#
# if __name__ == '__main__':
#     print(Bakery.main_logics)


    # modified:   pipert2/core/base/flow.py
    # modified:   pipert2/core/base/routine.py
    # modified:   pipert2/core/base/routines/destination_routine.py
    # modified:   pipert2/core/base/routines/middle_routine.py
    # modified:   pipert2/utils/annotations.py
    # modified:   pipert2/utils/data_class/dataclasses.py
    # modified: pipert2 / core / base / message.py
    # modified: pipert2 / core / base / routine.py
    # modified: pipert2 / core / base / routines / destination_routine.py
    # modified: pipert2 / utils / annotations.py
    # pipert2 / utils / metaclasses /


