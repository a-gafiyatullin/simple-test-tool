import os
from abc import ABC, abstractmethod


class Executable(ABC):
    """
    Base class for all executable entities.


    ...

    Methods
    -------
    pre_exec(message)
        prepare for the stage
    exec(message)
        execute the main flow of the stage
    post_exec(message)
        finalize the stage
    """

    def __init__(self, interrupt_if_fail, pre_script_path, main_script_path, post_script_path):
        """
        Parameters
        ----------
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        pre_script_path : str
            script for pre_exec()
        main_script_path : str
            script for exec()
        post_script_path : str
            script for post_exec()
        """
        self._interrupt_if_fail = interrupt_if_fail

        if pre_script_path != "":
            if not os.path.exists(pre_script_path):
                raise FileNotFoundError("Executable: Path " + pre_script_path + " doesn't exist!")
        self._pre_script_path = pre_script_path
        if main_script_path != "":
            if not os.path.exists(main_script_path):
                raise FileNotFoundError("Executable: Path " + main_script_path + " doesn't exist!")
        self._main_script_path = main_script_path
        if post_script_path != "":
            if not os.path.exists(post_script_path):
                raise FileNotFoundError("Executable: Path " + post_script_path + " doesn't exist!")
        self._post_script_path = post_script_path

    @abstractmethod
    def exec(self):
        """
        Execute the stage.
        """
        raise NotImplemented('Executable: exec is not implemented!')

    @abstractmethod
    def pre_exec(self):
        """
        Execute the stage.
        """
        raise NotImplemented('Executable: pre_exec is not implemented!')

    @abstractmethod
    def post_exec(self):
        """
        Execute the stage.
        """
        raise NotImplemented('Executable: post_exec is not implemented!')

    def _get_interrupt_if_fail(self):
        """
        Return a convention about interrupting all stages because of an error at this stage.
        """
        return self._interrupt_if_fail
