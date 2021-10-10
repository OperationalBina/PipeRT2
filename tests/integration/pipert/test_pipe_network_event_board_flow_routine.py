import pytest
from multiprocessing import Manager
from pipert2 import Pipe, QueueNetwork, Wire
from tests.unit.pipert.core.utils.events_utils import START_EVENT
from tests.integration.utils.routines.user_input_source_routine import UserInputSourceRoutine
from tests.integration.utils.routines.data_assertion_destination_routine import DataAssertionDestinationRoutine

FIRST_ROUTINE_NAME = "R1"
SECOND_ROUTINE_NAME = "R2"

DATA_IN_PIPE = []

for i in range(10):
    DATA_IN_PIPE.append(
        {"val": i}
    )


@pytest.fixture()
def pipe_with_flow_with_input_output_validations_routines():
    manager = Manager()
    shared_process_dict = manager.dict()

    input_data_routine = UserInputSourceRoutine(name=FIRST_ROUTINE_NAME,
                                                data_to_send=DATA_IN_PIPE.copy())

    data_validation_routine = DataAssertionDestinationRoutine(name=SECOND_ROUTINE_NAME,
                                                              data_to_expect=DATA_IN_PIPE.copy(),
                                                              shared_process_dict=shared_process_dict)

    pipe = Pipe(network=QueueNetwork(max_queue_sizes=len(DATA_IN_PIPE)))

    pipe.create_flow("Flow1", True, input_data_routine, data_validation_routine)

    pipe.build()

    return pipe, input_data_routine, data_validation_routine


@pytest.fixture()
def pipe_with_2_flows_with_input_output_validations_routines():
    manager = Manager()
    shared_process_dict = manager.dict()

    input_data_routine = UserInputSourceRoutine(name=FIRST_ROUTINE_NAME,
                                                data_to_send=DATA_IN_PIPE)

    data_validation_routine = DataAssertionDestinationRoutine(name=SECOND_ROUTINE_NAME,
                                                              data_to_expect=DATA_IN_PIPE,
                                                              shared_process_dict=shared_process_dict)

    pipe = Pipe(network=QueueNetwork(max_queue_sizes=len(DATA_IN_PIPE)))

    pipe.create_flow("Flow1", False, input_data_routine)
    pipe.create_flow("Flow2", False, data_validation_routine)
    pipe.link(Wire(source=input_data_routine, destinations=(data_validation_routine, )))

    pipe.build()

    return pipe, input_data_routine, data_validation_routine


def test_pipe_start_flow_using_events_expecting_the_validation_routine_to_get_all_of_the_given_data(
        pipe_with_flow_with_input_output_validations_routines):

    pipe, input_routine, validation_routine = pipe_with_flow_with_input_output_validations_routines
    pipe.notify_event(START_EVENT.event_name)
    try:
        input_routine.does_data_sent.wait()
        pipe.join(to_kill=True)
    except TimeoutError:
        assert not validation_routine.is_data_equal.is_set(), validation_routine.get_error()
        assert False, "The pipe didn't join but no error was recognized"
    else:
        assert not validation_routine.is_data_equal.is_set(), validation_routine.get_error()


def test_pipe_start_2_flows_using_events_expecting_the_validation_routine_to_get_all_of_the_given_data(
        pipe_with_2_flows_with_input_output_validations_routines):

    pipe, input_routine, validation_routine = pipe_with_2_flows_with_input_output_validations_routines
    pipe.notify_event(START_EVENT.event_name)
    try:
        input_routine.does_data_sent.wait()
        pipe.join(to_kill=True)
    except TimeoutError:
        assert not validation_routine.is_data_equal.is_set(), validation_routine.get_error()
        assert False, "The pipe didn't join but no error was recognized"
    else:
        assert not validation_routine.is_data_equal.is_set(), validation_routine.get_error()
