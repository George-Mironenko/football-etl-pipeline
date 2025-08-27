import extract
import transform

from loging_etl import logger


if __name__ == '__main__':
    try:
        if transform.transform_football_data(
                extract.get_competitions()):

            logger.info("Успешный запуск ETL")

    except Exception as error:
        logger.critical(error)