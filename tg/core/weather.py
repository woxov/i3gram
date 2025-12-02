import requests


def get_weather(city: str) -> str:
    url = f"http://wttr.in/{city}?T"

    response = requests.get(url, timeout=5)
    response.raise_for_status()

    lines = response.text.splitlines()
    weather_info = "\n".join(lines[:7])

    return weather_info
