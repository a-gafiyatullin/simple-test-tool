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
        Stage.__init__(self, "", False, "", "Notification", False, "", "", "")
        self._loggers = loggers

    @abstractmethod
    def _send(self, text):
        """
        Send the information from logs.
        """
        raise NotImplemented('Notification: _send is not implemented!')

    def pre_exec(self):
        return True

    def exec(self):
        text = ""

        for logger in self._loggers:
            logger.close()
            file_path = logger.get_log_file_path()
            text = text + '\n' + Path(file_path).read_text()
        return self._send(text)

    def post_exec(self):
        return True
