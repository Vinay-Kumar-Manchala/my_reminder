import os
import logging
from logging.handlers import RotatingFileHandler

__log_path__ = "logs/"
__log_level__ = "INFO"
__max_bytes__ = 10000000
__handler_type__ = "rotating_file_handler"
_log_file_name__ = "Reminder_logs"
__backup_count__ = 10
complete_log_path = os.path.join(__log_path__, _log_file_name__)
if not os.path.isdir(__log_path__):
    os.makedirs(__log_path__)


def get_logger(
    log_file_name=complete_log_path,
    log_level=__log_level__,
    time_format="%Y-%m-%d %H:%M:%S",
    handler_type=__handler_type__,
    max_bytes=__max_bytes__,
    backup_count=__backup_count__,
):
    """
    Creates a rotating log
    """
    log_file = log_file_name + ".log"  # Fixed this line
    __logger__ = logging.getLogger(log_file_name)
    __logger__.setLevel(log_level.strip().upper())
    debug_formatter = (
        "%(asctime)s - %(levelname)-6s - %(name)s - "
        "[%(threadName)5s:%(filename)5s:%(funcName)5s():"  # Fixed this line
        "%(lineno)s] - %(message)s"
    )
    formatter_string = (
        "%(asctime)s - %(levelname)-6s - %(name)s - %(levelname)3s - %(message)s"
    )
    if log_level.strip().upper() == log_level:
        formatter_string = debug_formatter
    formatter = logging.Formatter(formatter_string, time_format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    if __logger__.hasHandlers():
        __logger__.handlers.clear()
    if str(handler_type).lower() == "rotating_file_handler":
        # Rotating File Handler
        handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        handler.setFormatter(formatter)
        if __logger__.hasHandlers():
            __logger__.handlers.clear()
        __logger__.addHandler(handler)
    else:
        # File Handler
        hdlr_service = logging.FileHandler(log_file)
        hdlr_service.setFormatter(formatter)
        if __logger__.hasHandlers():
            __logger__.handlers.clear()
        __logger__.addHandler(hdlr_service)
    return __logger__


logger = get_logger()