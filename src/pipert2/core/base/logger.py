from abc import ABC, abstractmethod


class PipeLogger(ABC):
    """An interface for loggers implementations in the pipe.
    Every logger that the user want to use in the pipe must follow this interface methods.

    """

    @abstractmethod
    def info(self, message: str):
        """Log a message with severity of 'INFO'.

        Args:
            message: Message to log.

        """

        raise NotImplementedError

    @abstractmethod
    def error(self, message: str):
        """Log a message with severity of 'ERROR'.

        Args:
            message: Message to log.

        """

        raise NotImplementedError

    @abstractmethod
    def debug(self, message: str):
        """Log a message with severity of 'DEBUG'.

        Args:
            message: Message to log.

        """

        raise NotImplementedError

    @abstractmethod
    def warning(self, message: str):
        """Log a message with severity of 'WARNING'.

        Args:
            message: Message to log.

        """

        raise NotImplementedError

    @abstractmethod
    def exception(self, message: str):
        """Log a message with severity of 'ERROR' with exception information.

        Args:
            message: Message to log.

        """

        raise NotImplementedError

    @abstractmethod
    def get_logger_child(self, child_name: str) -> 'PipeLogger':
        """Get a logger which is a descendant to this one.

        Args:
            child_name: The name of the descendant logger.

        """

        raise NotImplementedError
