from stage import Stage
from abc import ABC, abstractmethod


class Build(Stage, ABC):
    """
    Base class for all building systems.
    """

    def __init__(self, path, parent_module_name, interrupt_if_fail, is_logging, log_file_path, log_name):
        """
        Parameters
        ----------
        path : str
            an absolute path to directory with build file(Makefile and etc)
        parent_module_name: str
            a parent module name
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        is_logging : bool
            write messages to the log file or not
        log_file_path : str
            an absolute path to directory for the log file
        log_name : str
            a name of the log file
        """
        Stage.__init__(self, parent_module_name, interrupt_if_fail, log_file_path, log_name, is_logging)
        self._build_path = path

    @abstractmethod
    def _clean(self):
        """
        Clean build directory from junk files.
        """
        pass

    @abstractmethod
    def _build(self):
        """
        Build source code.
        """
        pass
