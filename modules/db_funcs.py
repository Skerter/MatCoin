import aiomysql
import os
import logging
import asyncio
from rich.logging import RichHandler

DB_HOST = "195.26.227.31"
DB_LOGIN = "matcoin_user"
DB_PASSWORD = "ya_daun_228"
DB_DATABASE = "matcoin"
SECRET_KEY = "matcoin_secret_438838fgdfh34yhgrry4354h452caszjnhgk3"

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
                await asyncio.sleep(10*attempt+1)
            else:
                logger.critical(f"Не удалось подключиться к базе данных после {retry_count} попыток.")

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

async def login_to_app(username: str, password: str):
    conn = await connect_db()
    try:
        async with conn.cursor() as cursor:
            query = """
                SELECT password FROM users WHERE username = %s
            """
            await cursor.execute(query, (username,))
            result_raw = await cursor.fetchone()

            if result_raw:
                stored_password = result_raw[0]
                if stored_password == password:
                    logger.info(f"Успешный вход для пользователя {username}")
                    return True
                else:
                    logger.warning(f"Неверный пароль для пользователя {username}")
                    return False
            else:
                logger.warning(f"Пользователь {username} не найден")
                return False

    except aiomysql.MySQLError as e:
        logger.error(f"Ошибка при работе с БД: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    logger.info(asyncio.run(login_to_app('sosal', '52')))