from collections import defaultdict
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

    def registrar(params_or_func):
        if callable(params_or_func):
            if (not hasattr(registrar, "last_params")) or (registrar.last_params is None):
                registrar.last_params = "default_key"
            class_name = re.search(' (.*)\\.', params_or_func.__str__()).group(1)
            registry[class_name][registrar.last_params].add(params_or_func)
            registrar.last_params = None
            return params_or_func
        else:
            registrar.last_params = params_or_func
            return registrar

    registrar.all = registry

    return registrar
