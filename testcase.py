import time
from pipert2 import SourceRoutine, DestinationRoutine, Pipe, START_EVENT_NAME, KILL_EVENT_NAME


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
src_routine.name = "Source"
src1_routine = src()
src1_routine.name = "Src2"

dst1 = dst()
dst1.name = "Destination"

dst2 = dst()
dst2.name = "ds1"

dst3 = dst()
dst3.name = "ds2"

pipe = Pipe(auto_pacing_mechanism=True)


pipe.create_flow("f1", True, src_routine, dst1)
# pipe.create_flow("f2", True, src1_routine, dst3)
#
# pipe.link(
#     Wire(source=src_routine, destinations=(dst1, dst2)),
#     Wire(source=src1_routine, destinations=(dst3,))
# )

pipe.build()

# pipe.notify_event(START_ROUTINE_LOGIC_NAME)
pipe.notify_event(START_EVENT_NAME)

time.sleep(3)

print("after sleep!")

pipe.notify_event(KILL_EVENT_NAME)

print("Kill")

pipe.join()


print("After join")


