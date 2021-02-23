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
            self.get_logger().set_execution_status(not self._get_interrupt_if_fail())
            return not self._get_interrupt_if_fail()

    def _build(self):
        cwd = os.getcwd()
        os.chdir(self._build_path)

        ret_status = True

        for target in self._build_targets:
            not_error = subprocess.run(['make', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if not_error.returncode == 0:
                self.log('target ' + target + ' build SUCCESS!')
            else:
                self.log('target ' + target + ' build ERROR!')
                if not self._get_interrupt_if_fail():
                    continue
                else:
                    self.get_logger().set_execution_status(False)
                    ret_status = False

        os.chdir(cwd)
        return ret_status
