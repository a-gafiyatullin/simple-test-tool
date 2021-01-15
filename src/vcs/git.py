import subprocess
from vcs.vcs import VCS
import os


class Git(VCS):

    def _update_directory(self, path):
        not_error = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if not_error.returncode == 0:
            self.log('update SUCCESS!')
            return True
        else:
            self.log('update ERROR!')
            self.get_logger().set_execution_status(not self._get_interrupt_if_fail())
            return not self._get_interrupt_if_fail()

    def add_for_commit(self, file_path, file_name):
        if file_path[-1] != os.sep:
            file_path += os.sep

        not_error = subprocess.run(['git', 'add', file_path + file_name], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        if not_error.returncode == 0:
            self._commit_msg += file_name
            return True
        else:
            self.log('cannot add ' + file_name + ' to commit!')
            self.get_logger().set_execution_status(not self._get_interrupt_if_fail())
            return not self._get_interrupt_if_fail()

    def commit_and_push(self):
        for vcs_path in self._vcs_paths:
            not_error = subprocess.run(['git', 'commit', '-m', self._commit_msg], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            if not_error.returncode != 0:
                self.log(vcs_path + ': commit ERROR!')
                if not self._get_interrupt_if_fail():
                    continue
                else:
                    self.get_logger().set_execution_status(False)
                    return False
            else:
                self.log(vcs_path + ': commit SUCCESS!')

            not_error = subprocess.run(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if not_error.returncode != 0:
                self.log(vcs_path + ': push ERROR!')
                if not self._get_interrupt_if_fail():
                    continue
                else:
                    self.get_logger().set_execution_status(False)
                    return False
            else:
                self.log(vcs_path + ': push SUCCESS!')

        return True
