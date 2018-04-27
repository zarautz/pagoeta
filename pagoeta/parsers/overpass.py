import datetime

from typing import NamedTuple

from .base import JsonParser


class Place(NamedTuple):
    id: int
    name: str


class OverpassParser(JsonParser):
    def parse(self) -> dict:
        return self.json
