import logging
from rich.logging import RichHandler
import os

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "app.log")

LOG_LEVEL = 20  # INFO

def configure_logger(name: str) -> logging.Logger:
    """Функция для конфигурирования логгеров."""
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(LOG_LEVEL)

        rich_handler = RichHandler()
        formatter_rich = logging.Formatter('%(message)s')
        rich_handler.setFormatter(formatter_rich)
        logger.addHandler(rich_handler)

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter_file = logging.Formatter('[%(asctime)s - %(levelname)s - %(module)s] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter_file)
        #logger.addHandler(file_handler)

    return logger
