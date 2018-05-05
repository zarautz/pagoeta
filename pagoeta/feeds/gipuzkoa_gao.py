import datetime

from typing import List, NamedTuple

from .base import BaseFeed, HtmlParser
from .typing import FeedRequest, FeedResponse


BASE_URL = 'https://ssl4.gipuzkoa.net'
ZARAUTZ_GAO_CODE = 113


class GaoBulletin(NamedTuple):
    date: datetime.date
    title: str
    url: str


class GipuzkoaGaoParser(HtmlParser):
    def parse(self, *, date: datetime.date) -> List[GaoBulletin]:
        output = []

        for li in self.tree.xpath('//li[@class="organismo"]'):
            if int(li.find('./a').get('name')) == ZARAUTZ_GAO_CODE:
                for item in li.find('./ul[@class="anuncios"]'):
                    output.append(GaoBulletin(
                        date,
                        item.find('./div[@class="titulo_anuncio"]').text.strip()[:-1],
                        item.find('./div[@class="enlace_html"]/a').get('href').replace('../../../../..', BASE_URL)
                    ))

        return output


class GipuzkoaGaoFeed(BaseFeed):
    parser = GipuzkoaGaoParser

    def prepare_requests(self) -> List[FeedRequest]:
        reqs = []
        locale_path, locale_prefix = ('euskera/gao', 'be') if self.locale == 'eu' else ('castell/bog', 'bc')

        for date in [d for d in self.dates if d.isoweekday() in range(1, 6)]:
            year, month, day = str(date.year), '{:02}'.format(date.month), '{:02}'.format(date.day)
            url = f'{BASE_URL}/{locale_path}/{year}/{month}/{day}/{locale_prefix}{year[-2:]}{month}{day}.htm'
            reqs.append(FeedRequest(url, {'date': date}))

        return reqs

    def process_responses(self, responses: List[FeedResponse]):
        import json

        def default(obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()

        return json.dumps([self.parser(content=res.content).parse(**res.config) for res in responses], default=default)
