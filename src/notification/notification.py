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
        Stage.__init__(self, "", False, "", "Notification", False, "", "", "", False)
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
            if (logger.get_only_fail_notification() and not logger.get_execution_status())\
                    or not logger.get_only_fail_notification():
                file_path = logger.get_log_file_path()
                self._send(Path(file_path).read_text())

        return True

    def post_exec(self):
        return True
