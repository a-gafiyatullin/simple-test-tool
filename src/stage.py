import logger
import executable
from abc import ABC


class Stage(executable.Executable, ABC):
    """
    Base class for all testing stages.


    ...

    Methods
    -------
    log(message)
        write a message to the specific log file using a parent module name.

    """

    def __init__(self, parent_module_name, interrupt_if_fail, log_file_path, log_name, is_logging):
        """
        Parameters
        ----------
        log_file_path : str
            an absolute path to directory for the log file
        log_name : str
            a name of the log file
        is_logging : bool
            write messages to the log file or not
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        parent_module_name: str
            a parent module name
        """
        executable.Executable.__init__(self, interrupt_if_fail)
        self._logger = logger.Logger(log_file_path, log_name, is_logging)
        self._parent_module_name = parent_module_name

    def log(self, message):
        """
        Write a message to the specific log file using a parent module name.

        Parameters
        ----------
        message : str
           a message for writing to the log file
        """
        self._logger.log(self._parent_module_name + ': ' + message)

    def get_log_file_path(self):
        """
        Return the log file path or None
        """
        return self._logger.get_log_file_path()
