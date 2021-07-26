import re
from collections import defaultdict
from functools import partial


def class_functions_dictionary():
    """Create a decorator for marking functions and storing them in a
    dictionary by their class and their marking signature

    Returns:
        Decorator that stores its functions in the 'all' attribute.

    Example usage:
        .. code-block:: python
            class Bakery:
                cooking_styles = class_functions_dictionary()

                @cooking_styles("indian")
                def indian_backing(self):
                    pass

                @cooking_styles("asian")
                def asian_backing(self):
                    pass

                @classmethod
                def get_events(cls):
                    return cls.events.all[cls.__name__]


            print(Bakery.get_events())  # {'indian': [<function Bakery.indian_backing at 0x7f8c4f339dc0>],
                                        #  'asian': [<function Bakery.asian_backing at 0x7f8c4f339e50>]})

    """

    registry = defaultdict(lambda: defaultdict(set))

    def key_registrar(key_or_function):
        if callable(key_or_function):
            # No key was given to the function, setting a defualt key
            return registrar(key="default_key", function=key_or_function)
        else:
            return partial(registrar, key=key_or_function)

    def registrar(function, key):
        # Get the class name from the function __str__ attribute using regular expression
        class_name = re.search(' (.*)\\.', function.__str__()).group(1)

        registry[class_name][key].add(function)
        return function

    key_registrar.all = registry

    return key_registrar
