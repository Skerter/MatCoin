import dotenv
import os
import logging
import asyncio
from rich.logging import RichHandler

dotenv.load_dotenv()
DEV_MODE = os.getenv('DEV_MODE')
DEV_MODE = True if DEV_MODE == "YES" else False

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "main.log")

tmp_folder = "./tmp"
os.makedirs(tmp_folder, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(),
        logging.FileHandler(log_file, encoding="utf-8")
    ]
)
logger = logging.getLogger("rich")