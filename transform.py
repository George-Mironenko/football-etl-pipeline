import pandas as pd
from loging_etl import logger


def transform_football_data(data_json: dict):
    """
    Функция для преобразования данных в DataFrame.
    :param data_json: Данные для преобразования
    :return: DataFrame
    """
    data = []

    try:
        competitions = data_json["competitions"]

        for i in competitions:
            id = i["id"]

            if not i["currentSeason"]:
                logger.warning("Пропущен id = %s так как значение i['currentSeason'] = Null", id)
                continue
            elif not i["area"]['id']:
                logger.warning("Пропущен id = %s так как значение i['area']['id'] = Null", id)
                continue
            else:
                data.append([
                    id,
                    i["area"]['id'],
                    i["name"],
                    i["emblem"],
                    i["plan"],
                    i["currentSeason"]['id'],
                    i["numberOfAvailableSeasons"],
                    i["lastUpdated"]
                ])
        logger.debug("Создание списка для dataframe")

        df =  pd.DataFrame(data, columns=[
            "id", "area_id", "name",
                    "emblem", "plan", "currentSeason_id",
            "numberOfAvailableSeasons", "lastUpdated"])
        logger.debug("Успешное создание dataframe")

        df["lastUpdated"] = pd.to_datetime(df["lastUpdated"]).dt.strftime('%Y-%m-%d')
        logger.debug("Создание столбца lastUpdated")

        # Избавляемся от Nan преобразовывая в None.
        df = df.reset_index(drop=True)
        logger.debug("Удалены все индексы")

        df = df.where(pd.notna(df), None)
        logger.debug("Преобразованы Nan в None")

        logger.info("Успешное преобразование данных.")

        df.to_csv('data.csv', index=False)

        logger.info("Успешное сохранение данных в формате csv")

    except Exception as error:
        logger.error(error)
