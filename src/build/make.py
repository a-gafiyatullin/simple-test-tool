from build.build import Build
import subprocess
import os


class Make(Build):
    def _clean(self):
        cwd = os.getcwd()
        os.chdir(self._build_path)

        not_error = subprocess.run(['make', 'clean'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(cwd)
        return True if not_error.returncode == 0 else False

    def _build(self):
        cwd = os.getcwd()
        os.chdir(self._build_path)

        not_error = subprocess.run(['make', 'all'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(cwd)
        return True if not_error.returncode == 0 else False

    def exec(self):
        not_error = self._clean()
        if not not_error:
            self.log('Make: clean ERROR!')
            return False
        else:
            self.log('Make: clean SUCCESS!')
        not_error = self._build()
        if not not_error:
            self.log('Make: build ERROR!')
            return False
        else:
            self.log('Make: build SUCCESS!')

        return True
