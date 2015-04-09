from django.conf import settings
from PIL import Image, ImageOps


def get_absolute_uri(relative_uri):
    protocol = 'https://' if settings.SESSION_COOKIE_SECURE else 'http://'
    return '%s%s%s' % (protocol, settings.SITE_HOST, relative_uri)


def resize_image(image, image_filter):
    if image_filter == 'square':
        image = ImageOps.fit(image, (150, 150), Image.ANTIALIAS)

    elif image_filter == 'small':
        image.thumbnail((320, 240), Image.ANTIALIAS)

    elif image_filter == 'medium':
        image.thumbnail((640, 480), Image.ANTIALIAS)

    elif image_filter == 'large':
        image.thumbnail((1024, 768), Image.ANTIALIAS)

    return image
