from apistar import App, Route


def welcome():
    return {
        'message': 'Welcome to the OpenZarautz API!'
    }


routes = [
    Route('/', method='GET', handler=welcome),
]

app = App(routes=routes)
