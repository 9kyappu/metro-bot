# -*- coding: utf-8 -*-

from pyrogram import Client

from utils import StateManager
from db import MetroController, UserController, SqliteDb
from core.config import APP_NAME, SQLITE_FILE


APP = Client(APP_NAME)
STATE_MANAGER = StateManager()
DB_CONTROLLER = SqliteDb(db_file=SQLITE_FILE)
METRO_CONTROLLER = MetroController(db=DB_CONTROLLER)
USER_CONTROLLER = UserController(db=DB_CONTROLLER)
