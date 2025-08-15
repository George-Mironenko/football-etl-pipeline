import extract
import transform
import load


if __name__ == '__main__':
    try:
        if load.load_football_data(
            transform.transform_football_data(
                extract.get_competitions())):
            print("Все норм")
    except Exception as error:
        print("ОЙ ", error)