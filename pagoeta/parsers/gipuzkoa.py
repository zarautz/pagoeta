import datetime

from typing import List, NamedTuple

from .base import HtmlParser


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
