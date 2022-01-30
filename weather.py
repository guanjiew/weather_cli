import argparse
import json
import sys
from configparser import ConfigParser
from urllib import parse, request, error

from color import *

SECRET_FILE = ".secrets.ini"
BASE_WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
PADDING = 20
REVERSE = "\033[;7m"
RESET = "\033[0m"


def _get_api_key():
    """Fetch the API key from INI configuration file.
    Expects a configuration file named ".secrets.ini" with structure:
        [weather_cli]
        api_key=<YOUR-OPENWEATHER-API-KEY>
    """
    config = ConfigParser()
    config.read(SECRET_FILE)
    return config["weather_cli"]["api_key"]


def read_user_cli_args():
    """Handles the CLI user interactions.
    Returns:
        argparse.Namespace: Populated namespace object
    """

    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    parser.add_argument(
        "city",
        nargs="+",
        type=str,
        help="Enter City Name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units",
    )

    return parser.parse_args()


def build_weather_query(city_input, imperial=False):
    """Builds the URL for an API request to OpenWeather's weather API.
    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether to use imperial units for temperature
    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url


def get_weather_data(weather_api):
    try:
        response = request.urlopen(weather_api)
    except error.HTTPError as err:
        if err.code == 401:
            sys.exit("Access denied. Please check your API key is valid.")
        elif err.code == 404:
            sys.exit("Can't find weather data for the input city")
        else:
            sys.exit("Something else is going wrong ...")
    weather_data = response.read()

    try:
        return json.loads(weather_data)
    except json.JSONDecodeError:
        sys.exit("Can't read the server response."
                 )


def display_weather_info(weather_data, imperial=False):
    """Prints formatted weather information about a city.
    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether or not to use imperial units for temperature
    More information at https://openweathermap.org/current#name
    """
    city = weather_data["name"]
    weather_description = weather_data["weather"][0]["description"]
    weather_code = weather_data["weather"][0]["id"]
    temperature = weather_data["main"]["temp"]

    change_color(REVERSE)
    print(f"{city:^{PADDING}}", end="")
    change_color(RESET)

    change_weather_color(weather_code)
    print(
        f"\t{weather_description.capitalize():^{PADDING}}",
        end=" ",
    )
    change_color(RESET)

    print(f"({temperature}°{'F' if imperial else 'C'})")


if __name__ == "__main__":
    cli_args = read_user_cli_args()
    query_url = build_weather_query(cli_args.city, cli_args.imperial)
    city_data = get_weather_data(query_url)
    # test_data = {'coord': {'lon': -74.006, 'lat': 40.7143},
    #              'weather': [{'id': 802, 'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}],
    #              'base': 'stations',
    #              'main': {'temp': 19.63, 'feels_like': 15.33, 'temp_min': 16.43, 'temp_max': 22.48, 'pressure': 1017,
    #                       'humidity': 59}, 'visibility': 10000, 'wind': {'speed': 3, 'deg': 298, 'gust': 8.99},
    #              'clouds': {'all': 25}, 'dt': 1643558197,
    #              'sys': {'type': 2, 'id': 2039034, 'country': 'US', 'sunrise': 1643544474, 'sunset': 1643580635},
    #              'timezone': -18000, 'id': 5128581, 'name': 'New York', 'cod': 200}
    display_weather_info(city_data)
