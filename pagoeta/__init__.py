from apistar import ASyncApp, Route, Include

from .handlers import forecast


def welcome():
    return {
        'message': 'Welcome to the OpenZarautz API!'
    }


routes = [
    Route('/', method='GET', handler=welcome),
    Include('/v2/forecast', name='forecast', routes=forecast.routes),
]

event_hooks = [
]

app = ASyncApp(routes=routes, event_hooks=event_hooks)
