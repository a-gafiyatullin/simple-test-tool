import subprocess
from vcs.vcs import VCS


class SVN(VCS):

    def exec(self):
        not_error = self._update()
        if not not_error:
            self.log('SVN: update ERROR!')
        else:
            self.log('SVN: update SUCCESS!')

        return not_error

    def _update_directory(self, path):
        not_error = subprocess.run(['svn', 'up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True if not_error.returncode == 0 else False

