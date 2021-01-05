from build.build import Build
import subprocess
import os


class Cmake(Build):
    _build_dir = 'build'

    def _clean(self):
        dest_path = self._build_path + os.sep + self._build_dir
        subprocess.run(['rm', '-rf', dest_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        cwd = os.getcwd()
        os.chdir(self._build_path)
        os.mkdir(dest_path)
        os.chdir(cwd)

        self.log('clean!')
        return True

    def _build(self):
        dest_path = self._build_path + os.sep + self._build_dir
        cwd = os.getcwd()
        os.chdir(dest_path)

        not_error = subprocess.run(['cmake', '..'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not_error.returncode == 0:
            not_error = subprocess.run(['make', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(cwd)
        if not_error.returncode == 0:
            self.log('build SUCCESS!')
            return True
        else:
            self.log('build ERROR!')
            return not self._get_interrupt_if_fail()
