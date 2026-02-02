import logging
from colorama import Fore, Style


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        if record.levelno in self.COLORS:
            record.levelname = (f"{self.COLORS[record.levelno]}"
                                f"{record.levelname}{Style.RESET_ALL}")
            record.msg = (f"{self.COLORS[record.levelno]}"
                          f"{record.msg}{Style.RESET_ALL}")
        return super().format(record)


class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        return not any(word in record.getMessage().lower()
                       for word in ['password', 'token', 'secret'])


formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y - %m - %d %H:%M:%S"
)

console_handler = logging.StreamHandler() # В консоль
file_handler = logging.FileHandler("logs/etl.log") # В Файл

logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO)

console_handler.setFormatter(ColoredFormatter())
file_handler.setFormatter(ColoredFormatter())

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.addFilter(SensitiveDataFilter())

# Запрет импорта через `from module import *`
__all__ = []