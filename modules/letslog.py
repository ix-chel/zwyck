import logging

class ErrorLogger:
    def __init__(self):
        pass
    def error_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)
        file_handler = logging.FileHandler('errorlog_heapdump.txt')
        file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.propagate = False
        return self.logger
    