import time
from pipert2 import Pipe, START_EVENT_NAME, KILL_EVENT_NAME
from tests.end_to_end.utils.routines.source_counter_routine import SourceCounterRoutine
from tests.end_to_end.utils.routines.destination_counter_routine import DestinationCounterRoutine

source_counter_routine = SourceCounterRoutine(20, "src")
source_counter_routine.routine_notify_durations_interval = 0.25

destination_counter_routine = DestinationCounterRoutine(12, "dst")
destination_counter_routine.routine_notify_durations_interval = 0.25

pipe = Pipe(auto_pacing_mechanism=True)
pipe.routine_synchroniser.updating_interval = 0.25

pipe.create_flow("f1", True, source_counter_routine, destination_counter_routine)
pipe.build()

pipe.notify_event(START_EVENT_NAME)

time.sleep(2)

pipe.notify_event(KILL_EVENT_NAME)
pipe.join()