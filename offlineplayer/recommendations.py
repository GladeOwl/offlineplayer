import requests
from api_token import TOKEN

raw_data: dict = {"artist": "Lauren Aquilina", "track": "King"}
url: str = "https://api.spotify.com/v1/search"
headers: dict = {"Authorization": f"Bearer {TOKEN.token}"}


def encode_url(data: dict):
    artist: str = "%20".join(x for x in data["artist"].split(" "))
    track: str = "%20".join(x for x in data["track"].split(" "))
    q: str = f"remaster%20artist:{artist}%20track:{track}"

    return q


params: dict = {"q": encode_url(raw_data), "type": "track"}

response: requests.Response = requests.get(url, headers=headers, params=params)
print(response.json())
