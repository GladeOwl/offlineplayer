import requests
from api_token import TOKEN


def api_get(endpoint: str, params: dict) -> requests.Response:
    url: str = "https://api.spotify.com/v1/" + endpoint
    headers: dict = {"Authorization": f"Bearer {TOKEN.token}"}
    response: requests.Response = requests.get(url=url, headers=headers, params=params)
    return response
