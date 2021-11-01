from typing import List
import multiprocessing as mp
from pipert2.utils.consts import UPDATE_FPS_NAME


class SynchronizerNode:
    def __init__(self,
                 routine_name: str,
                 flow_name: str,
                 nodes: List['SynchronizerNode'],
                 manager):

        self.name = routine_name
        self.flow_name = flow_name
        self.nodes: List = nodes

        self.father_nodes_fps = {}
        self.calculated_fps = False
        self.notified_delay_time = False
        self.update_fps = False

        self.fps = manager.Value('f', 0.0)
        self.original_fps: mp.Value = manager.Value('f', 0.0)

    def update_original_fps_by_real_time(self, calculate_realtime_fps: callable):
        """Update the original fps by callback.

        Args:
            calculate_realtime_fps: The calculate function.
        """

        if not self.update_fps:

            self.original_fps.value = calculate_realtime_fps(self.name)
            self.fps.value = self.original_fps.value

            for node in self.nodes:
                node.update_original_fps_by_real_time(calculate_realtime_fps)

            self.update_fps = True

    def update_fps_by_nodes(self):
        """Update the fps by all nodes.
        If the max fps of sub logic has lower value then my fps, then change the fps value to the lower.

        Returns:
            The current fps.

        """

        if len(self.nodes) > 0 and not self.calculated_fps:
            max_nodes_fps = max(self.nodes, key=lambda node: node.update_fps_by_nodes()).fps.value
            self.fps.value = min(self.fps.value, max_nodes_fps)

            self.calculated_fps = True

        return self.fps.value

    def update_fps_by_fathers(self, father_name: str = None, father_fps: int = None):
        """Update the current fps by the fathers of the current nodes.

        Args:
            father_name: The name of the father node.
            father_fps: The father's fps.
        """

        if father_name is not None and father_fps is not None:
            self.father_nodes_fps[father_name] = father_fps

            max_fathers_name = max(self.father_nodes_fps, key=self.father_nodes_fps.get)
            max_fathers_fps = self.father_nodes_fps[max_fathers_name]

            if max_fathers_fps < self.original_fps.value:
                self.fps.value = max_fathers_fps
            else:
                self.fps.value = self.original_fps.value

        for node in self.nodes:
            node.update_fps_by_fathers(self.name, self.fps.value)

    def notify_fps(self, notify_event: callable):
        """Notify the current fps with the callback function.

        Args:
            notify_event: The callback for notifying event.
        """

        for node in self.nodes:
            node.notify_fps(notify_event)

        if not self.notified_delay_time:
            notify_event(UPDATE_FPS_NAME,
                         {self.flow_name: [self.name]},
                         **{'fps': self.fps.value})

            self.notified_delay_time = True

    def reset(self):
        """Reset the node's flags.

        """

        for node in self.nodes:
            node.reset()

        self.notified_delay_time = False
        self.calculated_fps = False
