import pytest
from mock import Mock
from demo.const import RPC_ENDPOINT
from pipert2.core.base.rpc_pipe_wrapper import RPCPipeWrapper
from pipert2.utils.consts import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME


@pytest.fixture
def rpc_pipe_wrapper():
    return RPCPipeWrapper(pipe=Mock(), endpoint=RPC_ENDPOINT)


def test_start(rpc_pipe_wrapper):
    rpc_pipe_wrapper.start()
    pipe_mock: Mock = rpc_pipe_wrapper.pipe
    pipe_mock.notify_event.assert_called_with(event_name=START_EVENT_NAME)


def test_stop(rpc_pipe_wrapper):
    rpc_pipe_wrapper.pause()
    pipe_mock: Mock = rpc_pipe_wrapper.pipe
    pipe_mock.notify_event.assert_called_with(event_name=STOP_EVENT_NAME)


def test_kill(rpc_pipe_wrapper):
    rpc_pipe_wrapper.kill()
    pipe_mock: Mock = rpc_pipe_wrapper.pipe
    pipe_mock.notify_event.assert_called_with(event_name=KILL_EVENT_NAME)
