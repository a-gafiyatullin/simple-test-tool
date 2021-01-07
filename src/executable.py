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

    def __init__(self, interrupt_if_fail):
        """
        Parameters
        ----------
        interrupt_if_fail : bool
            interrupt the execution of the all stages if an error has occurred
        """
        self._interrupt_if_fail = interrupt_if_fail

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
