import subprocess
from vcs.vcs import VCS


class Git(VCS):

    def exec(self):
        not_error = self._update()
        if not not_error:
            self.log('Git: update ERROR!')
        else:
            self.log('Git: update SUCCESS!')
        return not_error

    def _update_directory(self, path):
        not_error = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not_error.returncode == 0:
            return True
        else:
            return False
