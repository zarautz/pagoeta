import hashlib
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_asset_path(instance, filename):
    split = filename.rsplit('.', 1)
    name = hashlib.sha1(str(uuid.uuid1())).hexdigest()
    extension = split[1]
    return '%s/%s.%s' % (instance.get_asset_directory(), name, extension)


class ImageManager(models.Manager):
    def visible(self):
        return self.filter(is_visible=True)


class Image(models.Model):
    hash = models.CharField(max_length=40, unique=True, blank=True)
    image = models.ImageField(upload_to=get_asset_path, null=True, blank=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_visible = models.BooleanField(_('Visible'), default=True)
    position = models.PositiveSmallIntegerField(_('Position'))

    objects = ImageManager()

    class Meta(object):
        ordering = ('position',)
        abstract = True

    def save(self, *args, **kwargs):
        self.hash = hashlib.sha1(self.image.url).hexdigest()
        super(Image, self).save(*args, **kwargs)

    def get_url(self):
        return self.image.url


class XeroxImage(models.Model):
    hash = models.CharField(max_length=40, unique=True)
    url = models.URLField(null=True, blank=True)

    class Meta(object):
        db_table = 'core_xerox_image'

    def save(self, *args, **kwargs):
        self.hash = hashlib.sha1(self.url).hexdigest()
        super(XeroxImage, self).save(*args, **kwargs)
