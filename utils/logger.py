import logging
import os
import sys
from logging.handlers import RotatingFileHandler

try:
    from colorlog import ColoredFormatter
    use_colors = True
except ImportError:
    use_colors = False

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "meow_logger.log")
max_size = 5 * 1024 * 1024  
backup_count = 5

logger = logging.getLogger("meow_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = False  

file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  

file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(file_formatter)

if use_colors:
    console_formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt='%H:%M:%S',
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red"
        }
    )
else:
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt='%H:%M:%S'
    )

console_handler.setFormatter(console_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


while current_size < max_size:
    logger.info("Мяу, я милый и пушистый! Приютишь меня?")
    current_size = os.path.getsize(log_file)

# if __name__ == "__main__":
#     logger.debug("Это отладочное сообщение (DEBUG)")
#     logger.info("Это информационное сообщение (INFO)")
#     logger.warning("Это предупреждение (WARNING)")
#     logger.error("Это ошибка (ERROR)")
#     logger.critical("Это критическая ошибка (CRITICAL)")
