import os
import subprocess
from stage import Stage
from abc import ABC, abstractmethod


class Build(Stage, ABC):
    """
    Base class for all building systems.
    """

    def __init__(self, path, parent_module_name, interrupt_if_fail, is_logging, log_file_path, stage_name, targets,
                 pre_script_path, main_script_path, post_script_path):
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
        pre_script_path : str
            script for pre_exec()
        main_script_path : str
            script for exec()
        post_script_path : str
            script for post_exec()
        """
        Stage.__init__(self, parent_module_name, interrupt_if_fail, log_file_path, stage_name, is_logging,
                       pre_script_path, main_script_path, post_script_path)
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
        if self._post_script_path != "":
            cwd = os.getcwd()
            os.chdir(self._build_path)

            build = subprocess.run(self._post_script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            os.chdir(cwd)
            if build.returncode != 0:
                self.log('execution ' + self._post_script_path + ' finished with ERROR!')
                return self._get_interrupt_if_fail()
            else:
                self.log('execution ' + self._post_script_path + ' finished with SUCCESS!')

        return True
