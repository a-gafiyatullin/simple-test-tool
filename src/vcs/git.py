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
            return False

    def add_for_commit(self, file_path, file_name):
        curr_dir = os.getcwd()
        os.chdir(file_path)

        if file_path[-1] != os.sep:
            file_path += os.sep

        not_error = subprocess.run(['git', 'add', file_path + file_name], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        os.chdir(curr_dir)
        if not_error.returncode == 0:
            self._commit_msg += file_name
            return True
        else:
            self.log('cannot add ' + file_name + ' to commit!')
            return not self._get_interrupt_if_fail()

    def commit_and_push(self):
        for vcs_path in self._vcs_paths:
            curr_dir = os.getcwd()
            os.chdir(vcs_path)

            not_error = subprocess.run(['git', 'commit', '-m', self._commit_msg], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            if not_error.returncode != 0:
                self.log(vcs_path + ': commit ERROR!')
                os.chdir(curr_dir)
                return not self._get_interrupt_if_fail()
            else:
                self.log(vcs_path + ': commit SUCCESS!')

            not_error = subprocess.run(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            os.chdir(curr_dir)
            if not_error.returncode != 0:
                self.log(vcs_path + ': push ERROR!')
                return not self._get_interrupt_if_fail()
            else:
                self.log(vcs_path + ': push SUCCESS!')
                return True
