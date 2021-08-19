import pytest
from mock import patch, Mock
from src.pipert2.core.base.payload import Payload

DATA = {
    "Frame": [1, 2, 3],
    "metadata": {"Name": "Mayo"}
}


@pytest.fixture()
def dummy_payload():
    payload = Payload(DATA)
    return payload


@pytest.fixture()
def encoded_payload(dummy_payload: Payload):
    encoder_mock = Mock()
    encoder_mock.encode.side_effect = lambda val: val
    dummy_payload.encode(encoder_mock)
    return dummy_payload


def test_encode_payload(dummy_payload: Payload):
    assert not dummy_payload.encoded
    encoder_mock = Mock()
    dummy_payload.encode(encoder_mock)

    encoder_mock.encode.assert_called_with(DATA)
    assert dummy_payload.encoded


def test_decode_payload(encoded_payload: Payload):
    assert encoded_payload.encoded
    decoder_mock = Mock()
    encoded_payload.decode(decoder_mock)

    decoder_mock.decode.assert_called_with(DATA)
    assert not encoded_payload.encoded



