from stage import Stage
from abc import ABC, abstractmethod


class VCS(Stage, ABC):
    """
    Base class for all CSV systems.
    """
    def __init__(self, paths, parent_module_name, interrupt_if_fail, is_logging, log_file_path, log_name):
        """
        Parameters
        ----------
        paths : list
            an absolute paths to directories with CSV systems
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
        self._vcs_paths = paths.copy()

    @abstractmethod
    def _update(self):
        """
        Update file in the CSV directory.
        """
        pass

