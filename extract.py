from requests import get

def get_competitions():
    url = "https://api.football-data.org/v4/competitions"
    try:
        response = get(url=url)
        response.raise_for_status()
    except Exception as error:
        print(error)
        return None
    else:
        return response.json()

print(get_competitions())