from django.conf import settings
from django.core.urlresolvers import reverse
from PIL import Image, ImageOps
from requests import get
from StringIO import StringIO


IMAGE_SIZES = {
    'q': {
        'verbose': 'square',
        'size': (150, 150),
    },
    'n': {
        'verbose': 'small',
        'size': (320, 240),
    },
    'z': {
        'verbose': 'medium',
        'size': (640, 480),
    },
    'b': {
        'verbose': 'large',
        'size': (1024, 768),
    },
}


def get_absolute_uri(relative_uri):
    protocol = 'https://' if settings.SESSION_COOKIE_SECURE else 'http://'
    return protocol + settings.SITE_HOST + relative_uri


def transform_external_image(image_url, target_size):
    """
    Gets an image from an URL and returns a transformed image.
    `Image.BICUBIC` gives enough quality here: http://blog.uploadcare.com/pillow-2-7-extended-release-notes/
    """
    image = Image.open(StringIO(get(image_url).content))

    if target_size == 'q':
        image = ImageOps.fit(image, IMAGE_SIZES['q']['size'], Image.BICUBIC)

    elif target_size in ('n', 'z', 'b'):
        image.thumbnail(IMAGE_SIZES[target_size]['size'], Image.BICUBIC)

    return image


def get_image_sources(image_type, hash):
    """
    Returns internal URLs to the different image sizes available.
    We use `string.replace()` to reduce calls to the Django `reverse()` function.
    """
    base_url = get_absolute_uri(reverse('image', args=(image_type, hash, 'q')))

    return {
        IMAGE_SIZES['q']['verbose']: base_url,
        IMAGE_SIZES['n']['verbose']: base_url.replace('_q', '_n'),
        IMAGE_SIZES['z']['verbose']: base_url.replace('_q', '_z'),
        IMAGE_SIZES['b']['verbose']: base_url.replace('_q', '_b'),
    }
