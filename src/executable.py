from abc import ABC, abstractmethod


class Executable(ABC):
    """
    Base class for all executable entities.


    ...

    Methods
    -------
    exec(message)
        Execute the stage.
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

    def _get_interrupt_if_fail(self):
        """
        Return a convention about interrupting all stages because of an error at this stage.
        """
        return self._interrupt_if_fail
