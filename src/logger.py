import os


class Logger:
    """
    Base class for all entities with the logging feature.


    ...

    Methods
    -------
    log(message)
        write a message to the specific log file.
    get_log_file_path()
        return the log file path or None

    """

    def __init__(self, log_file_dir, log_name, is_logging):
        """
        Parameters
        ----------
        log_file_dir : str
            an absolute path to directory for the log file
        log_name : str
            a name of the log file
        is_logging : bool
            write messages to the log file or not
        """

        self._is_logging = is_logging

        if self._is_logging:
            if os.path.exists(log_file_dir) and os.path.isdir(log_file_dir):
                if log_file_dir[-1] != os.sep:
                    log_file_dir += os.sep
                self._log_file_path = log_file_dir + log_name
                if os.path.exists(self._log_file_path):
                    raise FileExistsError("Logger: File " + log_name + " already exists!")
                self._log_file = open(self._log_file_path, 'w')
            else:
                raise FileNotFoundError("Logger: Directory " + log_file_dir + " doesn't exists!")
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
            self._log_file.write(message)

    def get_log_file_path(self):
        """
        Return the log file path or None
        """
        return self._log_file_path

    def __del__(self):
        """
        Close the log file.
        """
        if self._log_file is not None:
            self._log_file.close()

