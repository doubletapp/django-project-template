import logging
from datetime import datetime


class Formatter(logging.Formatter):
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    LOGLEVEL_COLORS = {'WARNING': YELLOW, 'INFO': GREEN, 'DEBUG': BLUE, 'CRITICAL': RED, 'ERROR': MAGENTA}

    COLOR_SEQ = '\033[1;%dm'
    RESET_SEQ = '\033[0m'

    @staticmethod
    def colorize(string, color):
        return f'{Formatter.COLOR_SEQ % (30 + color)}{string}{Formatter.RESET_SEQ}'

    def format(self, record):
        now = self.formatTime(record, '%Y-%m-%d %H:%M:%S')
        loglevel = record.levelname
        record.datetime = Formatter.colorize(f'[{now}]', Formatter.BLACK)
        record.loglevel = Formatter.colorize(f'[{loglevel}]', Formatter.LOGLEVEL_COLORS[loglevel])
        record.source = Formatter.colorize(f'{record.pathname}:{record.lineno}', Formatter.CYAN)
        return logging.Formatter.format(self, record)


log = logging.getLogger('api')
