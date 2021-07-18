from collections import defaultdict
from functools import partial
import re


def marking_functions_annotation():
    """Create a decorator for marking functions and storing them in a
    dictionary by their class and their marking signature

    Returns:
        Decorator that stores its functions in the 'all' attribute.

    Example usage:
        .. code-block:: python
            class Bakery:
                cooking_styles = marking_functions_annotation()

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

    def key_registrar(key):
        if callable(key):
            return registrar(key="default_key", function=key)
        else:
            return partial(registrar, key=key)

    def registrar(function, key):
        class_name = re.search(' (.*)\\.', function.__str__()).group(1)
        registry[class_name][key].add(function)
        return registrar

    key_registrar.all = registry

    return key_registrar
