import datetime

from typing import List, NamedTuple

from .base import HtmlParser


class TideTable(NamedTuple):
    date: datetime.date
    low: List[str]
    high: List[str]


class IngurumenaTidesParser(HtmlParser):
    def parse(self, *, dates: List[datetime.date]) -> List[TideTable]:
        output = []

        for row, tr in enumerate(self.tree.xpath('//table[@class="footable"]/tbody/tr')):
            cols = tr.findall('./td')
            row_date = datetime.datetime.strptime(cols[0].text.strip(), '%d/%m/%Y').date()

            if row_date in dates:
                tides = TideTable(row_date, [], [])

                for col, td in enumerate(cols[1:]):
                    text = td.text
                    if not text:
                        continue
                    """mod % 2 to detect even cols."""
                    if (col % 2) == 0:
                        tides.high.append(text.strip())
                    else:
                        tides.low.append(text.strip())

                output.append(tides)

        return output
