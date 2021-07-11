from collections import defaultdict


def marking_functions_annotation():
    """Create a decorator for marking functions and storing them in a dictionary

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


            print(Bakery.cooking_styles.all)  # {'indian': [<function Bakery.indian_backing at 0x7f8c4f339dc0>],
                                              #  'asian': [<function Bakery.asian_backing at 0x7f8c4f339e50>]})

    """

    registry = defaultdict(list)

    def registrar(params_or_func):
        if callable(params_or_func):
            if (not hasattr(registrar, "last_params")) or (registrar.last_params is None):
                registrar.last_params = "default_key"
            registry[registrar.last_params].append(params_or_func)
            registrar.last_params = None
            return params_or_func
        else:
            registrar.last_params = params_or_func
            return registrar

    registrar.all = registry
    return registrar
