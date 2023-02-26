# -*- coding: utf-8 -*-

from pydantic import BaseModel


class SearchedStation(BaseModel):
    station_id: int
    name: str
