import os

import ETL.extract as extract
import ETL.transform as transform
from loging_etl import logger


def save_to_csv(df, path):
    try:
        # Создаем директорию если её нет
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Сохраняем в CSV
        df.to_csv(path, index=False, encoding='utf-8')
        logger.info(f"Данные успешно сохранены в: {path}")
        return True
    except Exception as error:
        logger.error(f"Ошибка при сохранении CSV: {error}")
        return False


if __name__ == '__main__':
    try:
        # Извлекаем данные
        raw_data = extract.get_competitions()
        if not raw_data:
            logger.error("Не удалось получить данные из API")
            exit(1)

        # Преобразуем данные
        df = transform.transform_football_data(raw_data)
        if df is None or df.empty:
            logger.error("Не удалось преобразовать данные")
            exit(1)

        output_path = os.getenv('OUTPUT_PATH', '/app/data/competitions.csv')
        if save_to_csv(df, output_path):
            logger.info("ETL процесс успешно завершен!")

    except Exception as error:
        logger.critical(error)