import asyncio
import datetime
import json

from aiohttp import ClientSession
from typing import Dict, List

from pagoeta.feeds.base import BaseFeed
from pagoeta.feeds.typing import FeedRequest, FeedResponse


class BaseSpider:
    requests: Dict[BaseFeed, List[FeedRequest]] = {}

    @staticmethod
    def json_default(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

    @staticmethod
    def get_feeds() -> List[BaseFeed]:
        raise NotImplementedError

    def process_responses(self, responses: List[FeedResponse]):
        raise NotImplementedError

    async def fetch(self, session: ClientSession, feed: BaseFeed, req: FeedRequest):
        async with session.request(req.method, req.url, data=req.data) as response:
            res = FeedResponse(await response.read(), req.config)
            return feed.process_response(response=res)

    async def run(self):
        tasks = []

        async with ClientSession() as session:
            for feed in self.get_feeds():
                for req in feed.prepare_requests():
                    t = asyncio.ensure_future(self.fetch(session, feed, req))
                    tasks.append(t)

            responses = await asyncio.gather(*tasks)
            return json.dumps(self.process_responses(responses), default=self.json_default)
