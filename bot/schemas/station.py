# -*- coding: utf-8 -*-

from pydantic import BaseModel


class StationModel(BaseModel):
    station_id: int
    name: str
