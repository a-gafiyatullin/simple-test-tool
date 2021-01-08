from build.build import Build
import subprocess
import os


class Custom(Build):

    def _clean(self):
        if self._pre_script_path != "":
            cwd = os.getcwd()
            os.chdir(self._build_path)

            build = subprocess.run(self._pre_script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            os.chdir(cwd)
            if build.returncode != 0:
                self.log('execution ' + self._pre_script_path + ' finished with ERROR!')
                return self._get_interrupt_if_fail()
            else:
                self.log('execution ' + self._pre_script_path + ' finished with SUCCESS!')

        return True

    def _build(self):
        if self._main_script_path != "":
            cwd = os.getcwd()
            os.chdir(self._build_path)

            build = subprocess.run(self._main_script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            os.chdir(cwd)
            if build.returncode != 0:
                self.log('execution ' + self._main_script_path + ' finished with ERROR!')
                return self._get_interrupt_if_fail()
            else:
                self.log('execution ' + self._main_script_path + ' finished with SUCCESS!')

        return True
