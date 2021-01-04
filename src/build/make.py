from build.build import Build
import subprocess
import os


class Make(Build):

    def _clean(self):
        cwd = os.getcwd()
        os.chdir(self._build_path)

        not_error = subprocess.run(['make', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(cwd)

        self.log('clean!')
        if not_error.returncode == 0:
            return True
        else:
            return not self._get_interrupt_if_fail()

    def _build(self):
        cwd = os.getcwd()
        os.chdir(self._build_path)

        not_error = subprocess.run(['make', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(cwd)
        if not_error.returncode == 0:
            self.log('build SUCCESS!')
            return True
        else:
            self.log('build ERROR!')
            return not self._get_interrupt_if_fail()
