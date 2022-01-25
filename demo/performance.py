import itertools
import time
import numpy as np
from pipert2 import Pipe, SourceRoutine, MiddleRoutine, DestinationRoutine, Data, QueueNetwork, \
    SharedMemoryTransmitter, START_EVENT_NAME, Wire
import plots


class A(SourceRoutine):
    def __init__(self, data_type: str, locked_fps: int = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.locked_fps = locked_fps
        self.data_type = data_type
        self.logic_counter = 0
        self.main_logic_fps = None
        self.logic_start = None
        self.transfer_data = {"frame": np.zeros(shape=(750, 520, 3), dtype=np.uint8),
                              "time": time.time()} if data_type == "frame" else {"time": time.time()}

    def main_logic(self) -> Data:
        data = Data()

        data.additional_data = self.transfer_data

        if self.logic_counter == 0:
            self.logic_start = time.time()

        if self.put_logic_counter == 0:
            self.put_and_logic_start = time.time()

        self.logic_counter += 1

        if self.locked_fps != 0:
            time.sleep(1 / self.locked_fps)

        if self.put_and_logic_fps is not None:
            data.additional_data["A"] = self.put_and_logic_fps

        if self.logic_counter == 1000:
            self.logic_counter = 0
            data.additional_data["A"] = self.put_and_logic_fps

        data.additional_data["msg_time"] = time.time()
        return data


class B(DestinationRoutine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.r_counter = 0
        self.start = None
        self.a_to_b_list = []

    def main_logic(self, data) -> Data:
        if self.r_counter == 0:
            self.start = time.time()

        self.r_counter += 1

        self.a_to_b_list.append(time.time() - data.additional_data["msg_time"])

        if self.r_counter == 1000:
            fps = 1 / ((time.time() - self.start) / self.r_counter)
            self.r_counter = 0

            if data.additional_data.get("A") is not None:
                data.additional_data["plot_data"] = {"A": data.additional_data["A"], "B": fps}
                print("write to file")

                with open("fps.txt", mode="w") as f:
                    f.write(str(data.additional_data["plot_data"]))

                with open("travel_time.txt", mode="w") as f:
                    f.write(str(self.a_to_b_list))

        return data


class C(DestinationRoutine):
    def main_logic(self, data: Data) -> None:
        x = 1500


def create_test_pipe(third_routine: bool, share_process: bool, data_type: str, locked_fps: int):
    pipe = Pipe(network=QueueNetwork(get_block=True), data_transmitter=SharedMemoryTransmitter(),
                auto_pacing_mechanism=False)

    source = A(data_type, locked_fps)
    middle = B()

    if share_process:
        pipe.create_flow("Test", False, source, middle)
    else:
        pipe.create_flow("Test", False, source)
        pipe.create_flow("Second", False, middle)

    if third_routine:
        third_routine = C()
        pipe.create_flow("Third", False, third_routine)
        pipe.link(Wire(source=source, destinations=(middle, third_routine)))
    else:
        pipe.link(Wire(source=source, destinations=(middle,)))

    pipe.build()

    return pipe


if __name__ == '__main__':
    params = {
        'third_routine_options': [True, False],
        'share_process_options': [True, False],
        'data_type_options': ["frame", "simple_data"],
        'locked_fps_options': [0, 50]
    }

    for params_option in itertools.product(*list(params.values())):
        pipe = create_test_pipe(*params_option)
        pipe.notify_event(START_EVENT_NAME)

        time.sleep(60)

        pipe.join(to_kill=True)
        print('finished join')

        plot_name = ''
        for key, option in zip(list(params.keys()), params_option):
            plot_name += f'{key}={str(option)},   '

        print(f'plot_name {plot_name}')
        plots.create_plot_fps(plot_name)
        plots.create_plot_travel_time(plot_name)
