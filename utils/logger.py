import logging


class Logger:
    def __init__(self, source):
        self.source = source

    def info(self, message):
        print(f"[{self.source}]: {message}")

    def log(self, message):
        print(f"[{self.source}]: {message}")

    def warn(self, message):
        logging.warn(f"[{self.source}]: {message}")

    def error(self, message):
        logging.error(f"[{self.source}]: {message}")
