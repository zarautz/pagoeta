from django.conf import settings
from PIL import Image, ImageOps


IMAGE_SIZES = {
    'square': (150, 150),
    'small': (320, 240),
    'medium': (640, 480),
    'large': (1024, 768),
}


def get_absolute_uri(relative_uri):
    protocol = 'https://' if settings.SESSION_COOKIE_SECURE else 'http://'
    return protocol + settings.SITE_HOST + relative_uri


def resize_image(image, image_filter):
    if image_filter == 'square':
        image = ImageOps.fit(image, IMAGE_SIZES['square'], Image.ANTIALIAS)

    elif image_filter in ('small', 'medium', 'large'):
        image.thumbnail(IMAGE_SIZES[image_filter], Image.ANTIALIAS)

    return image
