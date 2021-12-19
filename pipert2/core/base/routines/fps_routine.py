import time
from abc import ABCMeta
from pipert2.core.base.routine import Routine
from pipert2.utils.batch_notifier import BatchNotifier
from pipert2.utils.annotations import class_functions_dictionary
from pipert2.utils.consts import NOTIFY_ROUTINE_DURATIONS_NAME, UPDATE_FPS_NAME, START_EVENT_NAME, STOP_EVENT_NAME
from pipert2.utils.consts.synchronise_routines import FPS_MULTIPLIER, ROUTINE_NOTIFY_DURATIONS_INTERVAL, NULL_FPS, \
    DURATIONS_MAX_SIZE


class FPSRoutine(Routine, metaclass=ABCMeta):

    events = class_functions_dictionary()

    def __init__(self, name: str = None):
        super().__init__(name)

        self._fps = NULL_FPS
        self._const_fps = NULL_FPS

        self.notifier = None

        self.last_duration = None

    def initialize(self, message_handler, event_notifier, **kwargs):
        """Initialize FPSRoutine and initialize the base class.

        Args:
            message_handler: The message handler.
            event_notifier: The callback for event notifying.
            **kwargs: More arguments.

        """

        super(FPSRoutine, self).initialize(message_handler, event_notifier)

        self.notifier = BatchNotifier(ROUTINE_NOTIFY_DURATIONS_INTERVAL,
                                      NOTIFY_ROUTINE_DURATIONS_NAME,
                                      event_notifier, self.name, DURATIONS_MAX_SIZE)

    def set_const_fps(self, fps):
        """Set const fps for routine.

        Args:
            fps: The require fps.

        """

        self._const_fps = fps

    def _run(self):
        """Run the routine logic with delaying by required fps.

        Returns:

        """

        self._extended_run()

        if self.last_duration is not None:
            self._delay_routine(self.last_duration)
            self.last_duration = None

    def _delay_routine(self, last_duration):
        """Delay the routine by required fps.

        Args:
            last_duration: The last duration time of the main logic.

        """

        if last_duration is not None and (self._fps > NULL_FPS or self._const_fps > NULL_FPS):
            required_fps = self._const_fps if self._const_fps > NULL_FPS else self._fps

            if (required_fps > 0) and last_duration < (1 / required_fps):
                time.sleep((1 / required_fps) - last_duration)

    def _run_main_logic_with_durations_updating(self, main_logic: callable):
        """Run main logic with updating durations queue.

        Args:
            main_logic: Main logic to run.

        Returns:
            (main logic result, the duration time of main logic)

        """

        start_time = time.time()

        result = main_logic()

        duration: float = time.time() - start_time

        if self._const_fps is not NULL_FPS:
            duration = 1 / self._const_fps

        self.last_duration = duration
        self.notifier.add_record(duration)

        return result

    @events(UPDATE_FPS_NAME)
    def update_delay_time(self, fps) -> None:
        """Update the routine's fps.

        """

        if fps > 0:
            self._fps = fps * FPS_MULTIPLIER

    @events(START_EVENT_NAME)
    def start_notifier(self) -> None:
        """Start the batch notifier.

        """

        self.notifier.start()

    @events(STOP_EVENT_NAME)
    def stop_notifier(self) -> None:
        """Stop the batch notifier.

        """

        self.notifier.stop()

    @classmethod
    def get_events(cls):
        """Get the events of the routine

        Returns:
            dict[str, list[Callback]]: The events callbacks mapped by their events

        """

        routine_fps_events = cls.events.all[FPSRoutine.__name__]
        for event_name, events_functions in routine_fps_events.items():
            cls.events.all[cls.__name__][event_name].update(events_functions)

        cls.events.all[cls.__name__].update(Routine.get_events())

        return cls.events.all[cls.__name__]
