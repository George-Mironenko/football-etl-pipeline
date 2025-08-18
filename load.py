from connect import DB

from loging_etl import logger


def load_football_data(data_frame) -> bool:
    if data_frame is None or data_frame.empty:
        logger.error("Нет данных для загрузки")
        return False

    # Создание таблицы
    create_table_query = """
    CREATE TABLE IF NOT EXISTS competitions (
        id INT PRIMARY KEY,
        area_id INT,
        name VARCHAR(255) NOT NULL,
        emblem TEXT,
        plan VARCHAR(50),
        currentSeason INT,
        numberOfAvailableSeasons INT,
        last_updated DATE
    );
    """

    # SQL-запрос на вставку
    insert_query = """
            INSERT INTO competitions(
                id, area_id, name, emblem, plan,
                currentSeason, numberOfAvailableSeasons, last_updated
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        # Создаём таблицу
        if not DB.execute_procedure(create_table_query):
            logger.error("Не удалось создать таблицу")
            return False

        logger.info("Мы создали таблицу для вставки")

        # Подготовка данных
        records = [tuple(row) for row in data_frame.values]

        DB.cursor.executemany(insert_query, records)
        DB.connection.commit()

        logger.debug("Мы успешно сохранили данные в бд")
        logger.debug("Успешно загружено {len(records)} записей")

        logger.info("Мы успешно загрузили данные в Postgres")

        return True

    except Exception as error:
        logger.error(f"Ошибка при вставке: {error}")
        return False
