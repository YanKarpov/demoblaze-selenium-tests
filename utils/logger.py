import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  

log_file = os.path.join(log_dir, "meow_logger.log")
max_size = 5 * 1024 * 1024  
backup_count = 5  

logger = logging.getLogger("meow_logger")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count, encoding="utf-8")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# тестировал рабобту ограничения лог файла
# while current_size < max_size:
#     logger.info("Мяу, я милый и пушистый! Приютишь меня?")
#     current_size = os.path.getsize(log_file)

# print(f"Лог файл {log_file} достиг размера {current_size / 1024 / 1024:.2f} MB.")