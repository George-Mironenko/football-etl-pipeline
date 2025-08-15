import os
import atexit
import logging

from dotenv import load_dotenv

from data_class import PostgresConnection


#Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#Загрузка переменных окружения
load_dotenv()

#Подключение к БД
try:
    DB = PostgresConnection(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    logger.info("Подключение к БД успешно")  # Теперь logger доступен!
except Exception as e:
    logger.critical(f"Ошибка подключения к БД: {e}")
    raise

#Автоматическое закрытие при выходе
atexit.register(DB._close)

#Запрет импорта через `from module import *`
__all__ = []

