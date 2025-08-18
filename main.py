import extract
import transform
import load
from loging_etl import logger


if __name__ == '__main__':
    try:
        if load.load_football_data(
            transform.transform_football_data(
                extract.get_competitions())):
            logger.info("Успешный запуск ETL")

    except Exception as error:
        logger.critical(error)