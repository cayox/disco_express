import logging
from logging.handlers import RotatingFileHandler
from threading import current_thread
import time


class CustomFormatter(logging.Formatter):
    """
    Custom formatter to include thread, file, line, log level, time, and message in the log output.
    """

    def format(self, record: logging.LogRecord) -> str:
        ct = current_thread()
        record.threadName = ct.name
        record.filename = record.filename
        record.lineno = record.lineno
        record.levelname = record.levelname
        record.asctime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(record.created)
        )
        return f"[{record.asctime}] [{record.threadName}] [{record.filename}:{record.lineno}] [{record.levelname}] {record.msg}"


def setup_basic_logger(log_file_path: str) -> None:
    """
    Configures the basic logging setup to use both terminal and rotating log file output with custom formatting.

    Args:
    log_file_path (str): Path to the log file.
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    # Clear all existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Stream handler for terminal logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(CustomFormatter())

    # File handler setup
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1048576, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(CustomFormatter())

    # Adding handlers to the root logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.CRITICAL)
