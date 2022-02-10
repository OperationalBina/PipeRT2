import mock
import pytest
from pytest_mock import MockerFixture
from werkzeug.datastructures import MultiDict
from pipert2.core.wrappers.api_wrapper import APIWrapper
from pipert2 import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME, Pipe


@pytest.fixture
def api_wrapper_with_mock_notify(mocker: MockerFixture):
    pipe: Pipe = mocker.MagicMock()
    pipe.get_event_notify = mocker.MagicMock()

    api_wrapper = APIWrapper(host="", port=0, pipe=pipe)
    api_wrapper.app = mocker.MagicMock()

    return api_wrapper


def test_get_pipe_structure(api_wrapper_with_mock_notify):
    _ = api_wrapper_with_mock_notify.get_pipe_structure()

    api_wrapper_with_mock_notify.pipe.get_pipe_structure.assert_called_once()


def test_run(api_wrapper_with_mock_notify, mocker: MockerFixture):

    api_wrapper_with_mock_notify.api_process = mocker.MagicMock()
    api_wrapper_with_mock_notify.run()

    api_wrapper_with_mock_notify.api_process.start.assert_called_once()


def test_start(api_wrapper_with_mock_notify):
    api_wrapper_with_mock_notify.start()

    api_wrapper_with_mock_notify.notify_callback.assert_called_with(START_EVENT_NAME)


def test_pause(api_wrapper_with_mock_notify):
    api_wrapper_with_mock_notify.pause()

    api_wrapper_with_mock_notify.notify_callback.assert_called_with(STOP_EVENT_NAME)


def test_kill(api_wrapper_with_mock_notify, mocker):

    with mock.patch("flask.request", mocker.MagicMock()):
        api_wrapper_with_mock_notify.kill()
        api_wrapper_with_mock_notify.notify_callback.assert_called_with(KILL_EVENT_NAME)


def test_routine_execute_without_kwargs(api_wrapper_with_mock_notify, mocker: MockerFixture):

    request_mock = mocker.MagicMock()
    request_mock.json = {}

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.routine_execute("test_routine", "test")
        api_wrapper_with_mock_notify.notify_callback.assert_called_with("test", specific_routine="test_routine")


def test_routine_execute_with_kwargs(api_wrapper_with_mock_notify, mocker: MockerFixture):
    request_mock = mocker.MagicMock()
    request_mock.json = {"extra_args": {
        "param": "test"
    }}

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.routine_execute("test_routine", "test")

        api_wrapper_with_mock_notify.notify_callback.assert_called_with("test",
                                                                        specific_routine="test_routine",
                                                                        param="test")


def test_routines_execute_without_kwargs(api_wrapper_with_mock_notify, mocker: MockerFixture):
    request_mock = mocker.MagicMock()
    request_mock.json = {}

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.routines_execute("test")

        api_wrapper_with_mock_notify.notify_callback.assert_called_with("test")


def test_routines_execute_with_kwargs(api_wrapper_with_mock_notify, mocker: MockerFixture):
    request_mock = mocker.MagicMock()
    request_mock.json = {"extra_args": {
        "param": "test"
    }}

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.routines_execute("test")

        api_wrapper_with_mock_notify.notify_callback.assert_called_with("test",
                                                                        param="test")
