import pandas as pd


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
            if not i["currentSeason"]:
                continue
            else:
                data.append([
                    i["id"],
                    i["area"]['id'],
                    i["name"],
                    i["emblem"],
                    i["plan"],
                    i["currentSeason"]['id'],
                    i["numberOfAvailableSeasons"],
                    i["lastUpdated"]
                ])
        df =  pd.DataFrame(data, columns=[
            "id", "area_id", "name",
                    "emblem", "plan", "currentSeason_id",
            "numberOfAvailableSeasons", "lastUpdated"])
        print("w", df.head(10))

        df["lastUpdated"] = pd.to_datetime(df["lastUpdated"]).dt.strftime('%Y-%m-%d')
        # Избавляемся от Nan преобразовывая в None.
        df = df.reset_index(drop=True)
        df = df.where(pd.notna(df), None)

        return df

    except Exception as error:
        print(error)
        return None