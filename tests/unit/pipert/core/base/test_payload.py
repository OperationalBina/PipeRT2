import pytest
from pipert2.core.base.payload import Payload

DATA = {
    "Frame": [1, 2, 3],
    "metadata": {"Name": "Mayo"}
}


@pytest.fixture()
def dummy_payload():
    payload = Payload(DATA)
    return payload
