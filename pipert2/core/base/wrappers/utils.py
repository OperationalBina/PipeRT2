import json


def parse_arguments(encoded_arguments):
    """Parses user arguments and handles no arguments scenario.

    """
    if encoded_arguments is None:
        return {}

    return json.loads(encoded_arguments)
