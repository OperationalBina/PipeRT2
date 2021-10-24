from pipert2.core.base.routine_delay_synchronizer import RoutineDelaySynchronizer


class DummySynchronizer(RoutineDelaySynchronizer):
    def run_synchronized(self, routine_callable: callable, routine_name: str):
        routine_callable()
