import hashlib

from django.core.cache import cache


class XeroxMachine(object):
    IMAGE_TYPE_IN_URL = 'x'
    cache_key = 'xerox-machine'
    data = {}

    def __init__(self):
        self.data = cache.get(self.cache_key, {})

    def add(self, image_source):
        hash = hashlib.sha1(image_source.encode('utf-8')).hexdigest()

        if hash not in self.data:
            self.data[hash] = image_source

        cache.set(self.cache_key, self.data, None)
        return hash

    def get(self, hash):
        return self.data[hash] if hash in self.data else 'https://dummyimage.com/128x128/2195f3/fff.jpg&text=Z'
