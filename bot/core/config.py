# -*- coding: utf-8 -*-

from json import loads as json_loads
from os import getenv
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

APP_NAME = getenv("APP_NAME")
SQLITE_FILE = getenv("SQLITE_FILE")
SPB_MAP = getenv("SPB_MAP")
MOSCOW_MAP = getenv("MOSCOW_MAP")
CITY_IDS = json_loads(getenv("CITY_IDS"))  # Example: ["1", "2"]
