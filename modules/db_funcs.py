import asyncio
import os
import aiomysql
import time

try:
    from modules.logger_config import configure_logger
except ModuleNotFoundError:
    from logger_config import configure_logger

DB_HOST = "195.26.227.31"
DB_LOGIN = "matcoin_user"
DB_PASSWORD = "ya_daun_228"
DB_DATABASE = "matcoin"

tmp_folder = "./tmp"
os.makedirs(tmp_folder, exist_ok=True)

log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
logger = configure_logger('DB')

async def open_connection():
    """Создаёт подключение к базе данных."""
    try:
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=3306,
            user=DB_LOGIN,
            password=DB_PASSWORD,
            db=DB_DATABASE,
            autocommit=True
        )
        return conn
    except Exception as e:
        logger.error(f"Ошибка при подключении к базе данных: {e}")
        return None

async def close_connection(conn : aiomysql.Connection):
    """Закрытие соединения с базой данных."""
    try:
        if conn:
            await conn.ensure_closed()
            logger.info("Соединение с базой данных закрыто.")
    except Exception as e:
        logger.error(f"Ошибка при закрытии соединения: {e}")

async def login_to_app(username: str, password: str):
    """Проверка входа пользователя."""
    logger.info(f"Проверяю {username} с паролем {password} в базе")
    conn = None
    try:
        conn = await open_connection()
        if conn is None:
            logger.error("Не удалось создать соединение для подключения к базе данных.")
            return False

        async with conn.cursor() as cursor:
            await cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            row = await cursor.fetchone()

            if row:
                stored_password = row[0]
                if stored_password == password:
                    logger.info(f"Успешный вход для пользователя {username}")
                    return True
                else:
                    logger.warning(f"Неверный пароль для пользователя {username}")
                    return False
            else:
                logger.warning(f"Пользователь {username} не найден")
                return False
    except Exception as e:
        logger.error(f"Ошибка при работе с БД: {e}")
        return False
    finally:
        await close_connection(conn)

async def username_exists(username: str) -> bool:
    """Проверка, существует ли юзернейм в базе данных."""
    logger.info(f"Ищу {username} в базе")
    conn = None
    try:
        conn = await open_connection()
        if conn is None:
            logger.error("Не удалось создать соединение для подключения к базе данных.")
            return False

        async with conn.cursor() as cursor:
            await cursor.execute("SELECT 1 FROM users WHERE username = %s LIMIT 1", (username,))
            row = await cursor.fetchone()

            if row:
                logger.info(f"Юзернейм {username} существует в базе.")
                return True
            else:
                logger.warning(f"Юзернейм {username} не найден в базе.")
                return False
    except Exception as e:
        logger.error(f"Ошибка при проверке юзернейма: {e}")
        return False
    finally:
        await close_connection(conn)

async def benchmark():
    async def test():
        if await username_exists('sosal'):
            logger.info("Юзернейм найден!")
            return await login_to_app('sosal', '52')
        else:
            logger.critical("Юзернейм не найден!")
        
    tasks = [test() for _ in range(100)]
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    
    logger.info(f'Все запросы выполнены за {end_time - start_time:.2f} секунд')
    logger.info(f'Результаты: {results}')

async def main():
    await benchmark()

if __name__ == "__main__":
    asyncio.run(main())