from requests import get
from loging_etl import logger


def get_competitions():
    """
    Эта функция, которая делает запрос на api и получает данные.
    :return:
    """
    url = "https://api.football-data.org/v4/competitions"
    try:
        response = get(url=url)
        response.raise_for_status()

    except Exception as error:
        logger.error(error)
        return None
    else:
        logger.info("Успешное извлеченные данных из API")
        return response.json()
