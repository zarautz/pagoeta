from django.db import transaction, IntegrityError

from pagoeta.apps.core.functions import get_image_sources
from pagoeta.apps.core.models import XeroxImage


class BaseScraper(object):
    updated = None

    def get_xerox_image_sources(self, image_source):
        try:
            with transaction.atomic():
                x = XeroxImage(url=image_source)
                x.save()
        except IntegrityError:
            pass

        return {
            'source': get_image_sources(XeroxImage.IMAGE_TYPE_IN_URL, x.hash)
        }
