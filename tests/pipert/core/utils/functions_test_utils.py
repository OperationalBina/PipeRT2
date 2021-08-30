import time

from typing import Callable, Any


def timeout_wrapper(func: Callable, expected_value: Any, timeout_duration: int = 3):
    """Trigger given function until it returns the expected value during the timeout duration

        Args:
            func (Callable): The function to execute.
            expected_value (Any): The value to expect from the function
            timeout_duration (int): Timeout in seconds

        Returns:
            bool: True if the func returned the expected value during the time, False otherwise

    """

    timeout = time.time() + timeout_duration
    while time.time() < timeout:
        if expected_value == func():
            return True

    return False
