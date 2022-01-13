import pytest
import mock
from pytest_mock import MockerFixture
from werkzeug.datastructures import MultiDict
from pipert2 import START_EVENT_NAME, STOP_EVENT_NAME, KILL_EVENT_NAME
from pipert2.core.base.wrappers.api_wrapper import APIWrapper


@pytest.fixture
def api_wrapper_with_mock_notify(mocker: MockerFixture):

    notify = mocker.MagicMock()

    api_wrapper = APIWrapper(host="", port=0, notify_callback=notify)
    api_wrapper.app = mocker.MagicMock()

    return api_wrapper


def test_run_api(api_wrapper_with_mock_notify):
    api_wrapper_with_mock_notify.host = "test_url"
    api_wrapper_with_mock_notify.port = "10"

    api_wrapper_with_mock_notify.run_api()

    assert list(api_wrapper_with_mock_notify.app.run.call_args)[1] == {"host": "test_url", "port": "10"}


def test_start(api_wrapper_with_mock_notify):
    api_wrapper_with_mock_notify.start()

    api_wrapper_with_mock_notify.notify_callback.assert_called_with(START_EVENT_NAME)


def test_pause(api_wrapper_with_mock_notify):
    api_wrapper_with_mock_notify.pause()

    api_wrapper_with_mock_notify.notify_callback.assert_called_with(STOP_EVENT_NAME)


def test_kill(api_wrapper_with_mock_notify):
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
