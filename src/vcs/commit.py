from vcs.vcs import VCS
from stage import Stage
import filecmp


class Commit(Stage):
    """
    Base class for commit information.
    """

    def __init__(self, auto_commit_and_push, parent_module_name, is_logging, log_file_path, vcs_obj):
        """
        Parameters
        ----------
        parent_module_name: str
            a parent module name
        auto_commit_and_push : bool
            auto commit and push after notification stage
        is_logging : bool
            write messages to the log file or not
        log_file_path : str
            a path to directory for the log file
        vcs_obj : VCS
            VCS object
        """
        Stage.__init__(self, parent_module_name, False, log_file_path, 'Commit', is_logging)
        self._vcs_obj = vcs_obj
        self._auto_commit_and_push = auto_commit_and_push

    def diff(self, src_file_path, dst_file_path):
        """
        Binary compare src_file_path and dst_file_path, return True if they are equal.

        Parameters
        ----------
        src_file_path : str
            source file path
        dst_file_path : str
            destination file path
        """
        result = filecmp.cmp(src_file_path, dst_file_path)
        if not result:
            self.log(src_file_path + ' is NEW!')

        return result

    def get_vcs_obj(self):
        return self._vcs_obj

    def exec(self):
        if self._auto_commit_and_push:
            self._vcs_obj.commit_and_push()
