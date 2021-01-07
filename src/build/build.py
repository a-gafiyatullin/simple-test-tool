import os
from stage import Stage
from abc import ABC, abstractmethod


class Build(Stage, ABC):
    """
    Base class for all building systems.
    """

    def __init__(self, path, parent_module_name, interrupt_if_fail, is_logging, log_file_path, stage_name, targets):
        """
        Parameters
        ----------
        path : str
            a path to directory with build file(Makefile and etc)
        parent_module_name: str
            a parent module name
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        is_logging : bool
            write messages to the log file or not
        log_file_path : str
            a path to directory for the log file
        stage_name : str
            stage name
        targets : list
            list of targets to build
        """
        Stage.__init__(self, parent_module_name, interrupt_if_fail, log_file_path, stage_name, is_logging)
        self._build_path = path
        if self._build_path[-1] != os.sep:
            self._build_path += os.sep
        self._build_targets = targets.copy()

        if not os.path.exists(self._build_path):
            raise FileNotFoundError("Build: Directory " + self._build_path + " doesn't exists!")

    @abstractmethod
    def _clean(self):
        """
        Clean build directory from junk files.
        """
        raise NotImplemented('Build: _clean is not implemented!')

    @abstractmethod
    def _build(self):
        """
        Build source code.
        """
        raise NotImplemented('Build: _build is not implemented!')

    def pre_exec(self):
        return self._clean()

    def exec(self):
        return self._build()

    def post_exec(self):
        return True
