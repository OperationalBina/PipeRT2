from src.pipert2 import SourceRoutine


class StartDemo(SourceRoutine):

    def __init__(self):
        super().__init__()
        self.counter = None

    def main_logic(self) -> dict:
        print(f"Source {self.counter}")

        self.counter += 1

        return {
            "counter_first": self.counter,
            "counter_second": self.counter
        }

    def setup(self) -> None:
        self.counter = 0

    def cleanup(self) -> None:
        self.counter = None
