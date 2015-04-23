from django.conf import settings
from django.core.urlresolvers import reverse
from PIL import Image, ImageOps


IMAGE_SIZES = {
    'q': (150, 150),   # square
    'n': (320, 240),   # small
    'z': (640, 480),   # medium
    'b': (1024, 768),  # large
}


def get_absolute_uri(relative_uri):
    protocol = 'https://' if settings.SESSION_COOKIE_SECURE else 'http://'
    return protocol + settings.SITE_HOST + relative_uri


def resize_image(image, size):
    if size == 'q':
        image = ImageOps.fit(image, IMAGE_SIZES['q'], Image.ANTIALIAS)

    elif size in ('n', 'z', 'b'):
        image.thumbnail(IMAGE_SIZES[size], Image.ANTIALIAS)

    return image


def get_image_sources(source, hash):
    sources = {
        'event': 'e',
        'place': 'p',
        'xerox': 'x',
    }

    # We use `string.replace()` to reduce calls to the Django `reverse()` function
    base_url = get_absolute_uri(reverse('image', args=(sources[source], hash, 'q')))

    return {
        'square': base_url,
        'small': base_url.replace('_q', '_n'),
        'medium': base_url.replace('_q', '_z'),
        'large': base_url.replace('_q', '_b'),
    }
