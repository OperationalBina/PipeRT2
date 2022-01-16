import mock
import pytest
from pytest_mock import MockerFixture
from werkzeug.datastructures import MultiDict
from pipert2.core.wrappers import APIWrapper
from pipert2 import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME, Pipe


@pytest.fixture
def api_wrapper_with_mock_notify(mocker: MockerFixture):
    pipe: Pipe = mocker.MagicMock()
    pipe.get_event_notify = mocker.MagicMock()

    api_wrapper = APIWrapper(host="", port=0, pipe=pipe)
    api_wrapper.app = mocker.MagicMock()

    return api_wrapper


def test_run_api(api_wrapper_with_mock_notify, mocker: MockerFixture):

    api_wrapper_with_mock_notify.api_process = mocker.MagicMock()
    api_wrapper_with_mock_notify.run_api()

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


def test_execute_without_kwargs(api_wrapper_with_mock_notify, mocker: MockerFixture):

    request_mock = mocker.MagicMock()

    args = MultiDict()
    args.add("event_name", "test")

    request_mock.args = args

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.execute()
        api_wrapper_with_mock_notify.notify_callback.assert_called_with(event_name="test")


def test_execute_with_kwargs(api_wrapper_with_mock_notify, mocker: MockerFixture):

    request_mock = mocker.MagicMock()

    args = MultiDict()
    args.add("event_name", "test")
    args.add("external_params", "param")

    request_mock.args = args

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.execute()
        api_wrapper_with_mock_notify.notify_callback.assert_called_with(event_name="test", external_params="param")


def test_execute_with_kwargs_and_specific_flow_routines(api_wrapper_with_mock_notify, mocker: MockerFixture):

    request_mock = mocker.MagicMock()

    args = MultiDict()
    args.add("event_name", "test")
    args.add("external_params", "param")
    args.add("specific_flow_routines", {"a1": ["a2, a3"]})

    request_mock.args = args

    with mock.patch("flask.request", request_mock):
        api_wrapper_with_mock_notify.execute()
        api_wrapper_with_mock_notify.notify_callback.assert_called_with(event_name="test",
                                                                        external_params="param",
                                                                        specific_flow_routines={"a1": ["a2, a3"]})
