from typing import List

from pagoeta.feeds import BaseFeed, OverpassFeed
from pagoeta.feeds.typing import FeedResponse
from .base import BaseSpider


class PlacesSpider(BaseSpider):
    def __init__(self, *, types: List[str] = []) -> None:
        self.types = types

    def get_feeds(self) -> List[BaseFeed]:
        return [
            OverpassFeed(types=self.types),
        ]

    def process_responses(self, responses: List[FeedResponse]):
        return responses


class PlaceTypesSpider(PlacesSpider):
    pass
