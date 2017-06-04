import logging
import sys
from logging.handlers import RotatingFileHandler
from logging_formatter import LoggingFormatter
from stream_logger_handler import StreamLoggerHandler


class BaseLogger():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def create_logger(self, logger_name, log_file_path, log_format):
        logger = logging.getLogger(logger_name)
        logger.level = logging.DEBUG
        file_handler = RotatingFileHandler(log_file_path)
        formatter = LoggingFormatter(log_format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        if (sys.platform.startswith('win')):
            ch = StreamLoggerHandler(sys.stdout)
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger
