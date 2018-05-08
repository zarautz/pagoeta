import os

from apistar import ASyncApp, Route, Include

from .handlers import forecast, health, places


BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, 'static')


def welcome():
    return {
        'message': 'Welcome to the OpenZarautz API!'
    }


routes = [
    Route('/', method='GET', handler=welcome),
    Include('/v2/forecast', name='forecast', routes=forecast.routes),
    Include('/v2/health', name='health', routes=health.routes),
    Include('/v2/places', name='places', routes=places.routes),
]

event_hooks = [
]

app = ASyncApp(routes=routes, event_hooks=event_hooks, static_dir=STATIC_DIR, static_url='/')
