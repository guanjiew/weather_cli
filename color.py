PADDING = 20
# COLOUR SCHEME
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"
GREY = '\033[37m'
REVERSE = "\033[;7m"
RESET = "\033[0m"
# WEATHER CODE RANGE
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDS = range(801, 900)
# WEATHER COLOUR MAPPING


weather_color_mapping = {
    THUNDERSTORM: RED,
    DRIZZLE: CYAN,
    RAIN: BLUE,
    SNOW: WHITE,
    ATMOSPHERE: BLUE,
    CLEAR: YELLOW,
    CLOUDS: GREY
}


def change_color(color):
    print(color, end="")


def change_weather_color(code):
    for weather in weather_color_mapping:
        if code in weather:
            change_color(weather_color_mapping[weather])
            return
    change_color(RESET)
