# -*- coding: utf-8 -*-

from typing import List

from schemas import StationModel
from .queries import StationQuery
from .sqlite_db import SqliteDb


class MetroController:
    def __init__(self, db: SqliteDb):
        self._db = db
        self._city_names = {}
        self._metro = {}
        self._stations = {}
        self._all_data = {}

    async def init_metro(self, city_ids: List[str]):
        for city_id in city_ids:
            self._city_names[city_id] = (await self._db.execute(
                query=StationQuery.GET_CITY_DATA,
                parameters=(city_id, )
            ))[0][1]

            self._stations[city_id] = await self._db.execute(
                query=StationQuery.GET_CITY_METRO,
                parameters=(city_id, )
            )

            self._all_data[city_id] = await self._db.execute(
                query=StationQuery.GET_ALL_DATA,
                parameters=(city_id, )
            )
            self._metro[city_id] = self._generate_metro(
                stations=self._stations[city_id]
            )

    async def get_nodes(self, city_id: str) -> dict:
        return self._stations[city_id]

    async def get_all_data(self, city_id: str) -> dict:
        return self._all_data[city_id]

    async def search_stations(
            self,
            text: str,
            city_id: str) -> List[StationModel]:
        response = await self._db.execute(
            query=StationQuery.SEARCH_STATION,
            parameters=(city_id, f"%{text}%")
        )

        return [
            StationModel(
                station_id=station[0],
                line_id=station[2],
                name=station[3]
            ) for station in response
        ]

    async def get_city_name(self, city_id: str) -> str:
        return self._city_names.get(city_id)

    async def get_station_data(
            self,
            station_id: int,
            city_id: str) -> str:
        return self._metro[city_id][station_id]

    def _generate_metro(self, stations: List[tuple]) -> dict:
        return {
            station_id: StationModel(
                station_id=station_id,
                line_id=line_id,
                name=name
            ) for station_id, city_id, line_id, name in stations
        }
