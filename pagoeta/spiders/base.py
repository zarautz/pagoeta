import asyncio
import datetime

from aiohttp import ClientSession
from typing import Dict, List

from pagoeta.feeds.base import BaseFeed
from pagoeta.feeds.typing import FeedRequest, FeedResponse


class BaseSpider:
    feed_classes: List[BaseFeed] = []
    requests: Dict[BaseFeed, List[FeedRequest]] = {}

    def __init__(self, *, dates: List[datetime.date] = [], locale: str = 'eu') -> None:
        self.dates = dates
        self.locale = locale
        self.feeds = [feed_class(dates=dates, locale=locale) for feed_class in self.feed_classes]

    def process_responses(self, responses: List[FeedResponse]):
        raise NotImplementedError

    async def fetch(self, session: ClientSession, feed: BaseFeed, req: FeedRequest):
        async with session.request(req.method, req.url, data=req.data) as response:
            res = FeedResponse(await response.read(), req.config)
            return feed.process_response(response=res)

    async def run(self):
        tasks = []

        async with ClientSession() as session:
            for feed in self.feeds:
                for req in feed.prepare_requests():
                    t = asyncio.ensure_future(self.fetch(session, feed, req))
                    tasks.append(t)

            responses = await asyncio.gather(*tasks)
            return self.process_responses(responses)

    """
    def run(self):
        import requests

        responses = []

        with requests.Session() as session:
            for feed in self.feeds:
                for req in feed.prepare_requests():
                    res = session.request(req.method, req.url, data=req.data)
                    responses.append(feed.process_response(response=FeedResponse(res.content, req.config)))

        return self.process_responses(responses)
    """
