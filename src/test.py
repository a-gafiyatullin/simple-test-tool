from stage import Stage
import subprocess


class Test(Stage):
    """
    Class that containing and operating tests.
    """
    def __init__(self, script_paths, parent_module_name, interrupt_if_fail, is_logging, log_file_path, log_name):
        """
        Parameters
        ----------
        script_paths : list
            an absolute paths to tests
        parent_module_name: str
            a parent module name
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        is_logging : bool
            write messages to the log file or not
        log_file_path : str
            an absolute path to directory for the log file
        log_name : str
            a name of the log file
        """
        Stage.__init__(self, parent_module_name, interrupt_if_fail, log_file_path, log_name, is_logging)
        self.__script_paths = script_paths.copy()

    def _test(self):
        for test_path in self.__script_paths:
            test = subprocess.run(test_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            self.log("Test " + test_path + "\nStdout:\n:")
            self.log(test.stdout.decode('utf-8'))
            self.log("Stderr:\n:")
            self.log(test.stderr.decode('utf-8'))

            self.log("Test evaluated with code :" + str(test.returncode) + "\n")
            if test.returncode != 0 and self._get_interrupt_if_fail():
                return False

        return True

    def exec(self):
        return self._test()
