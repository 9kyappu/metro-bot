# -*- coding: utf-8 -*-

from pydantic import BaseModel


class SearchedStation(BaseModel):
    station_id: int
    name: str


class SearchedNode(BaseModel):
    name: str


class NamedStation(BaseModel):
    name: str
