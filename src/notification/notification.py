from stage import Stage
from abc import ABC, abstractmethod


class Notification(Stage, ABC):
    """
    Base class for all notification system.
    """
    def __init__(self, loggers):
        """
        Parameters
        ----------
        loggers: list
            list of loggers to send
        """
        Stage.__init__(self, "", False, "", "", False)
        self._loggers = loggers.copy()

    @abstractmethod
    def _send(self):
        """
        Send the information from logs.
        """
        pass
