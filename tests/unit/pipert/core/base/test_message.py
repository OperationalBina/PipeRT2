import pytest
from pytest_mock import MockerFixture
from pipert2.core.base.message import Message
from pipert2.utils.dummy_object import Dummy


MESSAGE_DATA = {"Feeling": "Good", "It's": "u", "Not no": "yes"}


@pytest.fixture()
def dummy_message(mocker: MockerFixture):
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

    assert all(entry_name == history_entry_name
               for entry_name, history_entry_name in zip(ENTRY_LIST, dummy_message.history.keys()))


def test_encode_message(mocker: MockerFixture, dummy_message: Message):
    mocker.patch("pickle.dumps")
    payload_mock = dummy_message.payload

    Message.encode(dummy_message)

    payload_mock.encode.assert_called()


def test_encode_message_when_unable_pickling(mocker: MockerFixture, dummy_message: Message):
    mocker.patch("pickle.dumps", side_effect=TypeError)
    payload_mock = dummy_message.payload

    encoded_msg = Message.encode(dummy_message)

    payload_mock.encode.assert_called()
    assert encoded_msg == dummy_message


def test_decode_message():
    message = Message(MESSAGE_DATA, "R1")
    message.payload = Dummy()
    message.payload.data = MESSAGE_DATA

    encoded_message = Message.encode(message)

    decoded_message:Message = Message.decode(encoded_message, lazy=False)

    assert decoded_message.__str__() == message.__str__()
