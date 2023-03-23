# -*- coding: utf-8 -*-

from .queries import UserQuery
from .sqlite_db import SqliteDb


class UserController:
    def __init__(self, db: SqliteDb):
        self._db = db

    async def create_user(self, user_id, date):
        try:
            await self._db.fill(
                query=UserQuery.INSERT_USER,
                parameters=(user_id, date, )
                )
            return
        except (Exception):
            pass

    async def search_city(
            self,
            user_id: int):
        response = await self._db.execute(
            query=UserQuery.GET_USER_DATA,
            parameters=(user_id, )
        )
        return response[0][1]

    async def set_city(self, city_id, user_id):
        try:
            await self._db.fill(
                query=UserQuery.INSERT_CITY,
                parameters=(city_id, user_id, )
                )
            return
        except (Exception):
            pass

    async def users_count(self):
        count_of_users = await self._db.execute(
            query=UserQuery.GET_USERS,
            parameters=None
        )
        return count_of_users[0]
