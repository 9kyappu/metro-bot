# -*- coding: utf-8 -*-

import asyncio

from core.app import APP, DB_CONTROLLER, METRO_CONTROLLER
from core.config import CITY_IDS

import handlers  # NOQA: F401


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(METRO_CONTROLLER.init_metro(CITY_IDS))
    APP.run()
finally:
    loop.run_until_complete(DB_CONTROLLER.close())
