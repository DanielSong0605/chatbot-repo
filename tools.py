from langchain_core.tools import tool
from datetime import datetime
import requests
import json
import wikipedia

information_file_path = "extra_info.json"


@tool
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    return a * b


@tool
def get_date() -> str:
    """Get the current date in the user's timezone."""

    return datetime.now().strftime("%a %b %d %Y")


@tool
def get_time() -> str:
    """Get the current time 24hr in the user's timezone in hours, minutes, seconds."""

    return datetime.now().strftime("%H:%M, %Ss")


@tool
def get_weather() -> str:
    """Get the temperature, apparent temperature, relative humidity, precipiation amount, surface pressure and wind speed at the user's location. Please analyze and format this information into an easy-to-understand description of the current conditions, explaining what each of the numbers means."""

    try:
        with open(information_file_path, 'r') as f:
            info = json.load(f)
            latitude, longitude, timezone = info["latitude"], info["longitude"], info["timezone"]
    except (FileNotFoundError, KeyError) as e:
        print(f"WARNING: Either {information_file_path} does not exist, or it does not contain the necessary keys. Using placeholder values.")
        latitude = 51.5085
        longitude = -0.1257
        timezone = "GMT"

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,surface_pressure,wind_speed_10m",
        "timezone": timezone,
        "forecast_days": 1
    }

    response = requests.get(url, params=params)

    data = response.json()
    current = data["current"]

    temp = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    apparent_temp = current["apparent_temperature"]
    precipitation = current["precipitation"]
    pressure = current["surface_pressure"]
    wind_speed = current["wind_speed_10m"]

    output = f"Temperature: {temp}C; Feels Like Temp: {apparent_temp}C; Relative Humidity: {humidity}%; Precipitation: {precipitation}mm; Surface Pressure: {pressure}hPa; Wind Speed: {wind_speed}km/h"
    
    return output


@tool
def get_summary(topic: str) -> str:
    """Get a summary of a Wikipedia page on the provided topic - similar to a Google search. ONLY use this function if you do not have any information on the topic, as it is very slow.
    
    Args:
        topic: Topic of Wikipedia summary
    """

    print("GETTING WIKIPEDIA SUMMARY ON:", topic)

    try:
        summary = wikipedia.summary(topic, auto_suggest=False)
    except wikipedia.PageError:
        try:
            summary = wikipedia.summary(topic, auto_suggest=True)
        except wikipedia.PageError:
            summary = "PageError: No such Wikipedia page exists"
        except wikipedia.DisambiguationError:
            summary = "DisambiguationError: Provided topic may refer to a number of pages"

    return summary


all_tools = [add, multiply, get_date, get_time, get_weather, get_summary]
