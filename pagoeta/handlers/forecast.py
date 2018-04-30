from apistar import Route

from pagoeta.spiders import SeaSpider
from pagoeta.utils import get_next_dates


async def get_sea_forecast() -> dict:
    return await SeaSpider(dates=get_next_dates(5)).run()


def list_weather_codes() -> list:
    return []


routes = [
    Route('/sea/', method='GET', handler=get_sea_forecast),
]
