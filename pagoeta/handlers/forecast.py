from apistar import Route

from pagoeta.spiders import SeaSpider, WeatherSpider


async def get_sea_forecast() -> dict:
    return await SeaSpider().run()


async def get_weather_forecast() -> dict:
    return await WeatherSpider().run()


def list_weather_codes() -> list:
    return []


routes = [
    Route('/sea/', method='GET', handler=get_sea_forecast),
    Route('/weather/', method='GET', handler=get_weather_forecast),
]
