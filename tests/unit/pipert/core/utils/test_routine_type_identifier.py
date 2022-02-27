from unittest.mock import Mock

from pipert2 import Wire
from pipert2.core.base.routines import FPSRoutine
from pipert2.utils.consts import GENERATOR_ROUTINE, INNER_ROUTINE, FINAL_ROUTINE
from pipert2.utils.routine_type_identifier import infer_routines_types


def test_infer_routines_types_1_gen_2_inner_1_final():
    routine_1 = Mock(spec=FPSRoutine)
    routine_2 = Mock(spec=FPSRoutine)
    routine_3 = Mock(spec=FPSRoutine)
    routine_4 = Mock(spec=FPSRoutine)

    wire_1 = Wire(source=routine_1, destinations=(routine_2, routine_3))
    wire_2 = Wire(source=routine_2, destinations=(routine_4,))
    wire_3 = Wire(source=routine_3, destinations=(routine_4,))

    given_wires = [wire_1, wire_2, wire_3]
    expected_result = {GENERATOR_ROUTINE: {routine_1},
                       INNER_ROUTINE: {routine_2, routine_3},
                       FINAL_ROUTINE: {routine_4}}

    actual_result = infer_routines_types(given_wires)

    assert expected_result == actual_result


def test_infer_routines_types_1_gen_2_inner_2_final():
    routine_1 = Mock(spec=FPSRoutine)
    routine_2 = Mock(spec=FPSRoutine)
    routine_3 = Mock(spec=FPSRoutine)
    routine_4 = Mock(spec=FPSRoutine)
    routine_5 = Mock(spec=FPSRoutine)

    wire_1 = Wire(source=routine_1, destinations=(routine_2, routine_3))
    wire_2 = Wire(source=routine_2, destinations=(routine_4,))
    wire_3 = Wire(source=routine_3, destinations=(routine_5,))

    given_wires = [wire_1, wire_2, wire_3]
    expected_result = {GENERATOR_ROUTINE: {routine_1},
                       INNER_ROUTINE: {routine_2, routine_3},
                       FINAL_ROUTINE: {routine_4, routine_5}}

    actual_result = infer_routines_types(given_wires)

    assert expected_result == actual_result


def test_infer_routines_types_1_gen_3_inner_2_final():
    routine_1 = Mock(spec=FPSRoutine)
    routine_2 = Mock(spec=FPSRoutine)
    routine_3 = Mock(spec=FPSRoutine)
    routine_4 = Mock(spec=FPSRoutine)
    routine_5 = Mock(spec=FPSRoutine)

    wire_1 = Wire(source=routine_1, destinations=(routine_2,))
    wire_2 = Wire(source=routine_2, destinations=(routine_3, routine_4))
    wire_3 = Wire(source=routine_3, destinations=(routine_5,))
    wire_4 = Wire(source=routine_4, destinations=(routine_5,))

    given_wires = [wire_1, wire_2, wire_3, wire_4]
    expected_result = {GENERATOR_ROUTINE: {routine_1},
                       INNER_ROUTINE: {routine_2, routine_3, routine_4},
                       FINAL_ROUTINE: {routine_5}}

    actual_result = infer_routines_types(given_wires)

    assert expected_result == actual_result


def test_infer_routines_types_multiple_inners():
    routine_1 = Mock(spec=FPSRoutine)
    routine_2 = Mock(spec=FPSRoutine)
    routine_3 = Mock(spec=FPSRoutine)
    routine_4 = Mock(spec=FPSRoutine)
    routine_5 = Mock(spec=FPSRoutine)

    wire_1 = Wire(source=routine_1, destinations=(routine_3,))
    wire_2 = Wire(source=routine_2, destinations=(routine_3, routine_4))
    wire_3 = Wire(source=routine_3, destinations=(routine_5,))
    wire_4 = Wire(source=routine_4, destinations=(routine_5,))

    given_wires = [wire_1, wire_2, wire_3, wire_4]
    expected_result = {GENERATOR_ROUTINE: {routine_1, routine_2},
                       INNER_ROUTINE: {routine_3, routine_4},
                       FINAL_ROUTINE: {routine_5}}

    actual_result = infer_routines_types(given_wires)

    assert expected_result == actual_result
