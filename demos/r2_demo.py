from src.pipert2 import MiddleRoutine


class R2(MiddleRoutine):
    def main_logic(self, data) -> dict:
        current_count = data["counter_second"] + 1

        return {
            "counter_second": current_count
        }

    def setup(self) -> None:
        print("Set up r2")

    def cleanup(self) -> None:
        print("Clean up r2")
