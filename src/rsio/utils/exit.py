from enum import IntEnum

class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    USAGE_ERROR = 2
    CONFIG_ERROR = 3
    DATA_ERROR = 4
    INTERRUPTED = 5
