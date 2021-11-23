from typing import List
from pipert2.utils.consts import UPDATE_FPS_NAME, NULL_FPS


class SynchroniserNode:
    """The SynchroniserNode is used in order to synchronise the fps throughout  the pipe.
     To achieve that, we need to synchronise each sub logic with each other.

    - The first step is updating the real fps of the current node.

    - The second step is calculating the minimum fps between {all the sub logics, take their max value}.
        When taking the max value of the sub logics, we handle the max fps that necessary.

    - The third step is calculating the minimum fps between {all the node owners, take their max value}.
        When taking the max value of the node owner, we handle the max fps that necessary from the owners.

    - The forth step is notifying the fps.

    - The fifth step is reset the flags. Because some node can be shared between two owners, and it already notified or
        updated with the realtime fps, then raise a flag for not notifying or updating twice.

    Simple Examples -
    Let's say A -> B -> C. A = 15, B = 10, C = 6. So the second step set the A,B = 6.
    Let's say A -> B -> C. A = 2, B = 5, C = 10. So the second step doesn't change a thing,
        and the third step set B,C = 2.
    """

    def __init__(self,
                 routine_name: str,
                 flow_name: str,
                 nodes: List['SynchroniserNode'] = []):

        self.name = routine_name
        self.flow_name = flow_name
        self.nodes: List = nodes

        self.father_nodes_fps = {}
        self.calculated_fps = False
        self.notified_delay_time = False
        self.update_fps = False

        self.curr_fps = NULL_FPS
        self.original_fps = NULL_FPS

    def update_original_fps_by_real_time(self, calculate_realtime_fps: callable):
        """Update the original fps by callback.

        Args:
            calculate_realtime_fps: The calculate function.

        """

        if not self.update_fps:

            self.original_fps = calculate_realtime_fps(self.name)
            self.curr_fps = self.original_fps

            for node in self.nodes:
                node.update_original_fps_by_real_time(calculate_realtime_fps)

            self.update_fps = True

    def update_fps_by_nodes(self):
        """Update the fps by all nodes.
        If the max fps of sub logic has lower value then the current fps, then change the fps value to the lower.

        Returns:
            The current fps.

        """

        if (len(self.nodes) > 0) and (not self.calculated_fps):
            max_nodes_fps = max(self.nodes, key=lambda node: node.update_fps_by_nodes()).curr_fps
            self.curr_fps = min(self.curr_fps, max_nodes_fps)
            self.calculated_fps = True

        return self.curr_fps

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

            if max_fathers_fps < self.original_fps:
                self.curr_fps = max_fathers_fps
            else:
                self.curr_fps = self.original_fps

        for node in self.nodes:
            node.update_fps_by_fathers(self.name, self.curr_fps)

    def notify_fps(self, notify_event: callable):
        """Notify the current fps with the callback function.

        Args:
            notify_event: The callback for notifying event.

        """

        if not self.notified_delay_time:
            notify_event(UPDATE_FPS_NAME, {self.flow_name: [self.name]}, fps=self.curr_fps)
            self.notified_delay_time = True

        for node in self.nodes:
            node.notify_fps(notify_event)

    def reset(self):
        """Reset the node's flags.

        """

        self.notified_delay_time = False
        self.calculated_fps = False
        self.update_fps = False

        for node in self.nodes:
            node.reset()
