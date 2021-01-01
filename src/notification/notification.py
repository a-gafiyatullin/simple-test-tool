from pathlib import Path
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
        self._loggers = loggers

    @abstractmethod
    def _send(self, text):
        """
        Send the information from logs.
        """
        raise NotImplemented('Notification: _send is not implemented!')

    def exec(self):
        text = ""

        for logger in self._loggers:
            file_path = logger.get_log_file_path()
            text = text + '\n' + Path(file_path).read_text()
        return self._send(text)
