import logging


class BaseLogger():
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def create_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.level = logging.DEBUG
        return logger
