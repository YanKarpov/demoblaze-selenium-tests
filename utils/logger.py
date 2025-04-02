import logging
import os
import glob

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

max_size = 5 * 1024 * 1024  

def get_next_log_file():
    existing_logs = sorted(glob.glob(os.path.join(log_dir, "meow_logger_*.log")))
    if existing_logs:
        last_log = existing_logs[-1]
        last_index = int(last_log.split("_")[-1].split(".")[0])
        new_index = last_index + 1
    else:
        new_index = 1
    return os.path.join(log_dir, f"meow_logger_{new_index}.log")

log_file = get_next_log_file()

logger = logging.getLogger("meow_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Форматирование логов
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

# Проверяем, если текущий файл уже полный, создаем новый
current_size = os.path.getsize(log_file) if os.path.exists(log_file) else 0

# тестировал рабобту ограничения лог файла
# while current_size < max_size:
#     logger.info("Мяу, я милый и пушистый! Приютишь меня?")
#     current_size = os.path.getsize(log_file)

# print(f"Лог файл {log_file} достиг размера {current_size / 1024 / 1024:.2f} MB.")