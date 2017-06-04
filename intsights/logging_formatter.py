import logging


class LoggingFormatter(logging.Formatter):

    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        result = logging.Formatter.format(self, record)
        return result
