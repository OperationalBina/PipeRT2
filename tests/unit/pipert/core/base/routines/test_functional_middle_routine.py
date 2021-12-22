import pytest
from pipert2.core.base.routines.functional_middle_routine import FunctionalMiddleRoutine

from pytest_mock import MockerFixture


@pytest.fixture
def functional_routine():
    return FunctionalMiddleRoutine(func=lambda x: x + 1)


@pytest.fixture
def mocked_func(mocker: MockerFixture):
    return mocker.MagicMock()


def test_functional_routine_logic(functional_routine):
    data = 2
    result = functional_routine.main_logic(data=data)

    assert result == 3


def test_functional_routine_execution(mocked_func):
    functional_routine = FunctionalMiddleRoutine(func=mocked_func)
    data = 2

    functional_routine.main_logic(data)
    mocked_func.assert_called_once_with(data)


def test_functional_routine_when_logic_is_changed(functional_routine):
    data = 2
    functional_routine.main_logic(data=data)

    return_value = 0
    functional_routine.logic = lambda x: return_value
    result = functional_routine.main_logic(data)

    assert result == return_value
