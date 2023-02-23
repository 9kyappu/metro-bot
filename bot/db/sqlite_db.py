# -*- coding: utf-8 -*-

import aiosqlite


class SqliteDb:
    def __init__(self, db_file: str):
        self._db_file = db_file
        self._db = None

    async def get_connect(self):
        if self._db is None:
            self._db = await aiosqlite.connect(self._db_file)
        return self._db

    async def close(self):
        if self._db is not None:
            await self._db.close()

    async def execute(self, query: str, parameters):
        db = await self.get_connect()

        async with db.cursor() as cursor:
            response = await cursor.execute(
                sql=query,
                parameters=parameters
            )
            return await response.fetchall()

    async def fill(self, query: str, parameters):
        db = await self.get_connect()

        async with db.cursor() as cursor:
            await cursor.execute(
                sql=query,
                parameters=parameters
            )
            await db.commit()
            return
