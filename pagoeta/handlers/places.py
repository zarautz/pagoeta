from apistar import Route

from pagoeta.spiders import PlacesSpider


async def get_place_types() -> dict:
    return await PlacesSpider().run()


routes = [
    Route('/types/', method='GET', handler=get_place_types),
]
