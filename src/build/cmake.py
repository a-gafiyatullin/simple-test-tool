from build.build import Build
import subprocess
import os


class Cmake(Build):
    _build_dir = 'build'

    def _clean(self):
        dest_path = self._build_path + os.sep + self._build_dir
        if os.path.exists(dest_path):
            cwd = os.getcwd()
            os.chdir(dest_path)

            not_error = subprocess.run(['rm', '-rf', dest_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if not_error.returncode == 0:
                os.mkdir(dest_path)

            os.chdir(cwd)
            return True if not_error.returncode == 0 else False
        else:
            return False

    def _build(self):
        dest_path = self._build_path + os.sep + self._build_dir
        cwd = os.getcwd()
        os.chdir(dest_path)

        not_error = subprocess.run(['cmake', '..'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if not_error.returncode == 0:
            not_error = subprocess.run(['make', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(cwd)
        return True if not_error.returncode == 0 else False

    def exec(self):
        not_error = self._clean()
        if not not_error:
            self.log('Cmake: clean ERROR!')
            return False
        else:
            self.log('Cmake: clean SUCCESS!')
        not_error = self._build()
        if not not_error:
            self.log('Cmake: build ERROR!')
            return False
        else:
            self.log('Cmake: build SUCCESS!')

        return True
