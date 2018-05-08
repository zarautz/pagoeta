from typing import List

from pagoeta.feeds import BaseFeed, CofgFeed, OverpassFeed
from pagoeta.feeds.typing import FeedResponse
from pagoeta.utils import get_next_dates
from .base import BaseSpider


class PharmaciesSpider(BaseSpider):
    @staticmethod
    def get_feeds() -> List[BaseFeed]:
        return [
            CofgFeed(dates=get_next_dates(2)),
            OverpassFeed(types=['amenity:pharmacy']),
        ]

    def process_responses(self, responses: List[FeedResponse]):
        return responses
