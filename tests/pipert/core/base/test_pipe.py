import pytest
from pytest_mock import MockerFixture

from src.pipert2.core.base.pipe import Pipe
from src.pipert2.utils.dummy_object import Dummy
from tests.pipert.core.utils.dummy_routine import DummyRoutine


@pytest.fixture()
def dummy_pipe(mocker: MockerFixture):
    pipe = Pipe(networking=mocker.Mock(), logger=mocker.Mock())

    return pipe


def test_get_data(dummy_pipe: Pipe, mocker: MockerFixture):
    FLOW_NAME = "f1"
    routine_mock = mocker.Mock()
    dummy_pipe.create_flow(FLOW_NAME, False, routine_mock)

    routine_mock.assert_called_once()

    assert
