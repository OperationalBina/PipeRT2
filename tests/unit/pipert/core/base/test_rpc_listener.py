import pytest
from mock import Mock, patch
from pipert2.core.base.rpc_listener import RPCListener
from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


@pytest.fixture
def rpc_listener():
    with patch('pipert2.core.base.pipe.Pipe') as mock_pipe:
        return RPCListener(mock_pipe)


def test_start(rpc_listener):
    rpc_listener.start()
    pipe_mock: Mock = rpc_listener.pipe
    pipe_mock.notify_event.assert_called_with(event_name=START_EVENT_NAME)


def test_stop(rpc_listener):
    rpc_listener.stop()
    pipe_mock: Mock = rpc_listener.pipe
    pipe_mock.notify_event.assert_called_with(event_name=STOP_EVENT_NAME)


def test_kill(rpc_listener):
    rpc_listener.kill()
    pipe_mock: Mock = rpc_listener.pipe
    pipe_mock.notify_event.assert_called_with(event_name=KILL_EVENT_NAME)
