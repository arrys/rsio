import os
import logging


def setup_logger(name, log_file, level=logging.INFO):
    """Setup of multiple loggers"""
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


class Logger(object):
    def __init__(self, name="customLogger", path=None, verbose=False):
        """Initialize a Logger component.

                Parameters
                ----------
                name : string
                    name of the property components

                verbose : bool
                    component verbose execution

                See Also
                --------
                ..

                Examples
                --------
                >> logger = Logger(verbose=False)

                """

        # --- logger configuration ---
        self._name = name
        self._verbose = verbose

        # set logging file
        if path is None:
            system_log = os.getcwd() + "/Resources/sys.log"
        else:
            system_log = path + "/Resources/sys.log"

        # setup logger
        self._syslogger = setup_logger(name="system_log", log_file=system_log, level=logging.INFO)
        # self.syslog(msg="Logger configured", level="INFO")

    @property
    def name(self):
        """The name property (read-only)."""
        return self._name

    def syslog(self, msg="tbd", level="INFO"):
        """Perform a system log entry.

            Parameters
            ----------
            msg : string
                message to be logged

            type : string
                Level of the logging


            See Also
            --------
            ..

            Examples
            --------
            >> logger.syslog(msg="this is a examples log message",level="INFO")

            """
        # verbose printing
        if self._verbose: print(msg)
        # logging
        if level == "INFO":
            self._syslogger.info(msg)
        elif level == "DEBUG":
            self._syslogger.debug(msg)
        elif level == "ERROR":
            self._syslogger.error(msg)
