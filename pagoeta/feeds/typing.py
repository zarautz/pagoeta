from typing import Any, NamedTuple


class FeedRequest(NamedTuple):
    url: str
    config: dict = {}
    method: str = 'GET'
    data: dict = {}


class FeedResponse(NamedTuple):
    content: Any
    config: dict = {}
