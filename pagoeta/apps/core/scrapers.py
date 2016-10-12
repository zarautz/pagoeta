from .functions import get_image_sources
from .helpers import XeroxMachine


class BaseScraper(object):
    updated = None

    def get_xerox_image_sources(self, image_source):
        x_hash = XeroxMachine().add(image_source)

        return {
            'source': get_image_sources(XeroxMachine.IMAGE_TYPE_IN_URL, x_hash)
        }
