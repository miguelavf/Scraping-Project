import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Initializes and configures a logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a handler to write log messages to stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger
