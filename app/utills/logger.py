import logging
import logging.handlers
import os


class Logger:
    """
    A logger class that sets up a logging configuration for an application.

    Attributes:
        _logger (logging.Logger): The configured logger instance.
    """

    def __init__(self, namespace="app"):
        """
        Initialize the Logger instance.

        Args:
            namespace (str): The namespace for the logger, default is "app".
        """
        file_name = namespace.replace(".log", "")
        logger = logging.getLogger(f"namespace.{file_name}")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            log_file = os.path.join(os.getcwd() + "/logs/app.log")
            if not os.path.exists(log_file):
                os.mkdir(os.path.join(os.getcwd() + "/logs/"))
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s %(name)s %(funcName)s %(levelname)s:%(message)s"
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self._logger
