import aiomysql
import dotenv
import os
import logging
import asyncio
from rich.logging import RichHandler

dotenv.load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_LOGIN = os.getenv('DB_LOGIN')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE')

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "db.log")

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

async def connect_db():
    """Попытка подключения к базе данных с повторными попытками (асинхронно)."""
    retry_count = 3
    for attempt in range(retry_count):
        try:
            conn = await aiomysql.connect(
                host=DB_HOST,
                user=DB_LOGIN,
                password=DB_PASSWORD,
                db=DB_DATABASE,
                charset='utf8mb4',
            )
            return conn
        except Exception as e:
            logger.error(f"Попытка {attempt+1} не удалась: {e}")
            if attempt < retry_count - 1:
                await asyncio.sleep(10*attempt)
            else:
                logger.critical(f"Не удалось подключиться к базе данных после {retry_count} попыток.")
                raise e

async def example_db_work():
    conn = await connect_db()
    try:
        async with conn.cursor() as cursor:
            query = """
                SELECT test_key FROM test LIMIT 1
            """
            await cursor.execute(query)
            result_raw = await cursor.fetchone()
            result = result_raw[0]
    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при работе с БД: {e}")
        result = "Ошибка при работе с БД"
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        result = "Неизвестная ошибка"
    finally:
        conn.close()
        return result

if __name__ == "__main__":
    logger.info(asyncio.run(example_db_work()))