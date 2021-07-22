import pytest
import pickle

from src.pipert2.core.base.message import Message

MESSAGE_DATA = {"Feeling": "Good", "It's": "u", "Not no": "yes"}


@pytest.fixture()
def dummy_message(mocker):
    msg = Message(data=MESSAGE_DATA, source_address="test_message")
    msg.payload = mocker.Mock()
    msg.payload.data = MESSAGE_DATA
    msg.payload.encoded = False

    return msg


def test_get_data(dummy_message: Message):
    assert dummy_message.get_data() == MESSAGE_DATA


def test_update_data(dummy_message: Message):
    NEW_DATA = {"new": "data"}
    dummy_message.update_data(NEW_DATA)
    assert dummy_message.get_data() == NEW_DATA


def test_record_entry(dummy_message: Message):
    ENTRY_LIST = ["R1", "R2", "R3", "R4", "R5"]
    for entry in ENTRY_LIST:
        dummy_message.record_entry(entry)

    print(dummy_message.history.keys())

    assert all(entry_name == history_entry_name
               for entry_name in ENTRY_LIST for history_entry_name in dummy_message.history.keys())


def test_encode_message(mocker, dummy_message: Message):
    payload_mock = mocker.Mock()
    dummy_message.payload = payload_mock

    encoded_message = Message.encode(dummy_message)

    payload_mock.encode.assert_called()
    assert encoded_message == pickle.dumps(dummy_message)


def test_decode_message(dummy_message: Message):
    encoded_message = Message.encode(dummy_message)

    decoded_message:Message = Message.decode(encoded_message, lazy=False)

    assert decoded_message.__str__() == encoded_message.__str__()
