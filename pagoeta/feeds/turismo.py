from typing import List, Dict

from .base import HtmlParser


class TurismoEvent(Dict):
    id: int
    name: str


class TurismoAgendaParser(HtmlParser):
    def parse(self) -> List[TurismoEvent]:
        data = []

        for li in self.tree.xpath('//*[@id="agendaIn"]//li[@class="rssRow odd"]'):
            title = li.find('.//a')
            data.append(TurismoEvent(
                id=int(title.get('href').split('=')[-1]),
                title=title.text
            ))

        return data


class TurismoEventParser(HtmlParser):
    def parse(self) -> TurismoEvent:
        return TurismoEvent()
