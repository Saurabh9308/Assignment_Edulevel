import logging
from logging.config import dictConfig


DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        }
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}


def setup_logging(config: dict | None = None):
    """
    Configure application wide logging. Pass a dictConfig-compatible
    structure to override the defaults in tests if needed.
    """
    dictConfig(config or DEFAULT_LOGGING_CONFIG)

