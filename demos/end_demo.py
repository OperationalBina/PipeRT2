from src.pipert2 import DestinationRoutine


class EndDemo(DestinationRoutine):
    def main_logic(self, data):
        print(data)

    def setup(self) -> None:
        print("Set up end")

    def cleanup(self) -> None:
        print("Clean up end")
