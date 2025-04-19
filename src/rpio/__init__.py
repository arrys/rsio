import logging
import arklog

# logger = logging.getLogger(__name__)
config = {
    "version": 1, "incremental": False, "disable_existing_loggers": False,
    "formatters": {"color": {"()": "arklog.ColorFormatter", "format": "%(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "level": "INFO", "formatter": "color"}},
    "root": {"level": "INFO", "handlers": ["console"], "propagate": True},
    # "loggers": {logger.name: {"level": "INFO", "handlers": ["console"], "propagate": False}},
}
arklog.set_config_logging(config)
