import time

from typing import List, NamedTuple

from .base import HtmlParser


class KostaImages(NamedTuple):
    snapshots: List[str]
    timex: List[str]


class KostaParser(HtmlParser):
    def parse(self) -> KostaImages:
        output = KostaImages([], [])

        for img in self.tree.xpath('//a[@class="monitorizaciones"]/img'):
            src = f'{img.get("src")}?{time.time()}'
            if 'snap.jpeg' in src:
                output.snapshots.append(src)
            else:
                output.timex.append(src)

        return output
