from src.pipert2 import MiddleRoutine


class R1(MiddleRoutine):
    def main_logic(self, data) -> dict:
        current_count = data["counter_first"] + 1

        return {
            "counter_first": current_count
        }

    def setup(self) -> None:
        print("Set up r1")

    def cleanup(self) -> None:
        print("Clean up r1")
