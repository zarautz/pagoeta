import json

from typing import List

from pagoeta.feeds import BaseFeed, AemetFeed, MagicseaweedFeed
from pagoeta.feeds.typing import FeedResponse
from pagoeta.utils import get_next_dates
from .base import BaseSpider


class WeatherSpider(BaseSpider):
    @staticmethod
    def get_feeds() -> List[BaseFeed]:
        dates = get_next_dates(5)
        return [
            AemetFeed(dates=dates),
            MagicseaweedFeed(dates=dates),
        ]

    def process_responses(self, responses: List[FeedResponse]):
        return responses
