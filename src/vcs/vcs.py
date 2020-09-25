from stage import Stage
from abc import ABC, abstractmethod
import os


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
    def _update_directory(self, path):
        """
        Update files in the CSV directory.
        """
        pass

    def _update(self):
        """
        Update files in the CSV directories.
        """
        cwd = os.getcwd()
        not_error = True
        for directory in self._vcs_paths:
            os.chdir(directory)
            not_error = self._update_directory(directory)
            if self._interrupt_if_fail and not not_error:
                break
        os.chdir(cwd)
        return not_error
