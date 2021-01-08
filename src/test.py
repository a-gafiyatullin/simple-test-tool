import os
from stage import Stage
import subprocess


class Test(Stage):
    """
    Class that containing and operating tests.
    """

    def __init__(self, script_path, parent_module_name, interrupt_if_fail, is_logging, log_file_path):
        """
        Parameters
        ----------
        script_path : str
            an absolute path to tests
        parent_module_name: str
            a parent module name
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        is_logging : bool
            write messages to the log file or not
        log_file_path : str
            an absolute path to directory for the log file
        """
        Stage.__init__(self, parent_module_name, interrupt_if_fail, log_file_path, 'Test', is_logging, "",
                       script_path, "")

    def pre_exec(self):
        return True

    def exec(self):
        test = subprocess.run(self._main_script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.log("Test " + self._main_script_path + "\nStdout:")
        self.log(test.stdout.decode('utf-8'))
        self.log("Stderr:")
        self.log(test.stderr.decode('utf-8'))

        self.log("Test finished with code " + str(test.returncode))
        if test.returncode != 0:
            return not self._get_interrupt_if_fail()

        return True

    def post_exec(self):
        return True
