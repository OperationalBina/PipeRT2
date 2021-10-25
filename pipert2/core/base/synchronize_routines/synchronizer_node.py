from typing import List


class SynchronizerNode:
    def __init__(self, name: str,
                 fps: int,
                 nodes: List['SynchronizerNode'],
                 notify_delay_time_callback: callable):

        self.fps = fps
        self.name = name
        self.nodes = nodes
        self.father_nodes_fps = {}
        self.notify_delay_time_callback = notify_delay_time_callback

        self.calculated_fps = False
        self.notified_delay_time = False

        self.original_fps = fps

    def update_fps_by_nodes(self):
        if len(self.nodes) > 0 and not self.calculated_fps:
            max_nodes_fps = max(self.nodes, key=lambda node: node.update_fps_by_nodes()).fps
            self.fps = min(self.fps, max_nodes_fps)
            self.calculated_fps = True

        return self.fps

    def update_fps_by_fathers(self, name: str = None, fps: int = None):
        # TODO - Think of a better name then a father
        if name is not None and fps is not None:
            self.father_nodes_fps[name] = fps
            max_fathers_fps_index = max(self.father_nodes_fps, key=self.father_nodes_fps.get)
            max_fathers_fps = self.father_nodes_fps[max_fathers_fps_index]

            if max_fathers_fps < self.original_fps:
                self.fps = max_fathers_fps
            else:
                self.fps = self.original_fps

        for node in self.nodes:
            node.update_fps_by_fathers(self.name, self.fps)

    def notify_fps(self):
        for node in self.nodes:
            node.notify_fps()

        if not self.notified_delay_time:
            self.notify_delay_time_callback(self.name, self.fps)
            self.notified_delay_time = True

    def reset(self):
        for node in self.nodes:
            node.reset()

        self.notified_delay_time = False
        self.calculated_fps = False
