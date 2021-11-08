import time

from pipert2 import SourceRoutine, DestinationRoutine, Pipe, Wire, START_EVENT_NAME, KILL_EVENT_NAME
from pipert2.utils.consts import FINISH_ROUTINE_LOGIC_NAME, START_ROUTINE_LOGIC_NAME


class src(SourceRoutine):
    def main_logic(self) -> dict:
        a = 5

        return {
            'a': 5
        }


class dst(DestinationRoutine):
    def main_logic(self, dict):
        a = 5

        time.sleep(1)


src_routine = src()
src_routine.name = "Src"
src1_routine = src()
src1_routine.name = "Src2"

dst1 = dst()
dst1.name = "dst"

dst2 = dst()
dst2.name = "ds1"

dst3 = dst()
dst3.name = "ds2"

pipe = Pipe(auto_pacing_mechanism=True)


pipe.create_flow("f1", True, src_routine, dst1)
# pipe.create_flow("f2", False, src1_routine, dst3)
#
# pipe.link(
#     Wire(source=src_routine, destinations=(dst1, dst2)),
#     Wire(source=src1_routine, destinations=(dst3,))
# )

pipe.build()

# pipe.notify_event(START_ROUTINE_LOGIC_NAME)
pipe.notify_event(START_EVENT_NAME)

time.sleep(3)

pipe.notify_event(KILL_EVENT_NAME)
pipe.join()
