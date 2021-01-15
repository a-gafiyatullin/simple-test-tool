import os
from datetime import date


class Logger:
    """
    Base class for all entities with the logging feature.


    ...

    Methods
    -------
    log(message)
        write a message to the specific log file
    get_log_file_path()
        return the log file path or None
    get_only_fail_notification()
        return notification condition
    set_execution_status(status)
        set execution status of the Stage
    get_execution_status()
        get execution status of the Stage
    """
    def __init__(self, log_file_dir, stage_name, is_logging, only_fail_notification):
        """
        Parameters
        ----------
        log_file_dir : str
            an absolute path to directory for the log file
        stage_name : str
            stage name
        is_logging : bool
            write messages to the log file or not
        only_fail_notification : bool
            notification condition
        """
        log_name = str(date.today()) + '-' + stage_name + '.txt'

        self._is_logging = is_logging
        self._only_fail_notification = only_fail_notification
        self._execution_status = True

        if self._is_logging:
            if os.path.exists(log_file_dir) and os.path.isdir(log_file_dir):
                if log_file_dir[-1] != os.sep:
                    log_file_dir += os.sep
                self._log_file_path = log_file_dir + log_name
                if os.path.exists(self._log_file_path):
                    self._log_file = open(self._log_file_path, 'a')
                else:
                    self._log_file = open(self._log_file_path, 'w')
            else:
                raise FileNotFoundError("Logger: Directory " + log_file_dir + " doesn't exist!")
        else:
            self._log_file = None
            self._log_file_path = None

    def log(self, message):
        """
        Write a message to the specific log file.

        Parameters
        ----------
        message : str
           a message for writing to the log file
        """
        if self._log_file is not None:
            self._log_file.write(message + '\n')

    def get_log_file_path(self):
        """
        Return the log file path or None.
        """
        return self._log_file_path

    def get_only_fail_notification(self):
        """
        Return notification condition.
        """
        return self._only_fail_notification

    def set_execution_status(self, status):
        """
        Set execution status.

        Parameters
        ----------
        status : bool
           new Stage execution
        """
        self._execution_status = status

    def get_execution_status(self):
        """
        Get execution status.
        """
        return self._execution_status

    def close(self):
        """
        Close the log file.
        """
        if self._log_file is not None:
            self._log_file.close()
