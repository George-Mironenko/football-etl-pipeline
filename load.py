# load.py
from connect import DB
import pandas as pd

def load_football_data(data_frame) -> bool:
    if data_frame is None or data_frame.empty:
        print("❌ Нет данных для загрузки")
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

    try:
        # Создаём таблицу
        if not DB.execute_procedure(create_table_query):
            print("❌ Не удалось создать таблицу")
            return False

        # Подготовка данных
        records = [tuple(row) for row in data_frame.where(pd.notna(data_frame), None).values]

        # SQL-запрос на вставку
        insert_query = """
        INSERT INTO competitions(
            id, area_id, name, emblem, plan,
            currentSeason, numberOfAvailableSeasons, last_updated
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            last_updated = EXCLUDED.last_updated;
        """

        # ✅ Ключевое исправление: используем executemany напрямую
        DB.cursor.executemany(insert_query, records)
        DB.connection.commit()  # ✅ Не забываем commit
        print(f"✅ Успешно загружено {len(records)} записей")
        return True

    except Exception as error:
        print(f"❌ Ошибка при вставке: {error}")
        DB.connection.rollback()  # ✅ Откат при ошибке
        return False