from apistar import Route

from pagoeta.spiders import PharmaciesSpider


async def get_pharmacies() -> dict:
    return await PharmaciesSpider().run()


routes = [
    Route('/pharmacies/', method='GET', handler=get_pharmacies),
]
