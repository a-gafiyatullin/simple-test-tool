from stage import Stage
from abc import ABC, abstractmethod
import os


class VCS(Stage, ABC):
    """
    Base class for all CSV systems.


    ...

    Methods
    -------
    add_for_commit(file_path, file_name)
        add new file in file_path to commit
    commit_and_push()
        commit and push added files
    """

    def __init__(self, paths, parent_module_name, interrupt_if_fail, is_logging, log_file_path, stage_name):
        """
        Parameters
        ----------
        paths : list
            paths to directories with CSV systems
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
        """
        Stage.__init__(self, parent_module_name, interrupt_if_fail, log_file_path, stage_name, is_logging, "", "", "")
        self._vcs_paths = paths.copy()
        for path in self._vcs_paths:
            if not os.path.exists(path):
                raise FileNotFoundError("VCS: Directory " + path + " doesn't exists!")
        self._commit_msg = 'new '

    @abstractmethod
    def _update_directory(self, path):
        """
        Update files in the CSV directory.
        """
        raise NotImplemented('VCS: _update_directory is not implemented!')

    def _update(self):
        """
        Update files in the CSV directories.
        """
        cwd = os.getcwd()

        not_error = True
        for directory in self._vcs_paths:
            os.chdir(directory)
            not_error = self._update_directory(directory)
            if not not_error:
                break

        os.chdir(cwd)
        return not_error

    @abstractmethod
    def add_for_commit(self, file_path, file_name):
        """
        Add new file in file_path to commit.


        Parameters
        ----------
        file_path : str
           a path to the file file_name
        file_name : str
            file name
        """
        raise NotImplemented('VCS: add_for_commit is not implemented!')

    @abstractmethod
    def commit_and_push(self):
        """
        Commit and push added files.
        """
        raise NotImplemented('VCS: commit_and_push is not implemented!')

    def pre_exec(self):
        return True

    def exec(self):
        return self._update()

    def post_exec(self):
        return True
