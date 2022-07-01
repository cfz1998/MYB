import logging
import colorlog

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    "WARNING": 'yellow',
    "ERROR": 'red',
    'CRITICAL': 'bold_red',
}

class Log:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s",
        log_colors=log_colors_config) 

    def console(self, level, message):
 
        # create a StreamHandler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
 
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
            
        self.logger.removeHandler(ch)

 
    def debug(self, message):
        self.console('debug', message)
 
    def info(self, message):
        self.console('info', message)
 
    def warning(self, message):
        self.console('warning', message)
 
    def error(self, message):
        self.console('error', message)

