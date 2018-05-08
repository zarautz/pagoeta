import datetime

from itertools import groupby
from typing import List, NamedTuple
from urllib.parse import urlencode

from .base import BaseFeed, HtmlParser
from .typing import FeedRequest, FeedResponse


class TideTable(NamedTuple):
    date: datetime.date
    low: List[str]
    high: List[str]


class GipuzkoaTidesParser(HtmlParser):
    def parse(self, *, dates: List[datetime.date]) -> List[TideTable]:
        output = []

        for tr in self.tree.xpath('//table[@class="footable"]/tbody/tr'):
            cols = tr.findall('./td')
            row_date = datetime.datetime.strptime(cols[0].text.strip(), '%d/%m/%Y').date()

            if row_date in dates:
                tides = TideTable(row_date, [], [])

                for col, td in enumerate(cols[1:]):
                    text = td.text
                    if not text:
                        continue

                    if (col % 2) == 0:
                        tides.high.append(text.strip())
                    else:
                        tides.low.append(text.strip())

                output.append(tides)

        return output


class GipuzkoaTidesFeed(BaseFeed):
    parser = GipuzkoaTidesParser

    def __init__(self, *, dates: List[datetime.date] = []) -> None:
        self.dates = dates

    def prepare_requests(self) -> List[FeedRequest]:
        reqs = []
        portlet = 'DCJmareas_WAR_DCJmareasportlet_INSTANCE_3Y41WFd6kR9h'
        months = [((date.year, date.month), date) for date in self.dates]

        for ym, group in groupby(months, key=lambda x: x[0]):
            dates = [el[1] for el in group]
            params = {
                'p_l_id': 613952,
                'p_p_id': portlet,
                f'_{portlet}_mes': ym[1],
                f'_{portlet}_anyo': ym[0]
            }
            url = f'http://www.gipuzkoaingurumena.eus/es/c/portal/layout?{urlencode(params)}'
            reqs.append(FeedRequest(url, {'dates': dates}))

        return reqs

    def process_response(self, response: FeedResponse):
        return self.parser(content=response.content).parse(**response.config)
