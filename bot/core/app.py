# -*- coding: utf-8 -*-

from os.path import exists as is_path_exists

from pyrogram import Client

from utils import StateManager
from db import MetroController, UserController, SqliteDb

from core.config import (
    APP_NAME,
    TG_API_ID,
    TG_API_HASH,
    BOT_TOKEN,
    SQLITE_FILE
)


_app_params = dict(
    api_id=TG_API_ID,
    api_hash=TG_API_HASH,
    bot_token=BOT_TOKEN
) if not is_path_exists(f"{APP_NAME}.session") else {}

APP = Client(
    name=APP_NAME,
    **_app_params
)

STATE_MANAGER = StateManager()
DB_CONTROLLER = SqliteDb(db_file=SQLITE_FILE)
METRO_CONTROLLER = MetroController(db=DB_CONTROLLER)
USER_CONTROLLER = UserController(db=DB_CONTROLLER)
