import hashlib
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from .functions import get_image_sources


def get_asset_path(instance, filename):
    split = filename.rsplit('.', 1)
    name = hashlib.sha1(str(uuid.uuid1())).hexdigest()
    extension = split[1]
    return '%s/%s.%s' % (instance.get_asset_directory(), name, extension)


class ImageManager(models.Manager):
    def visible(self):
        return self.filter(is_visible=True)


class Image(models.Model):
    IMAGE_TYPE_IN_URL = None
    hash = models.CharField(max_length=40, unique=True, blank=True)
    file = ProcessedImageField(upload_to=get_asset_path, null=True, blank=True,
                               verbose_name=_('label:file'),
                               processors=(ResizeToFit(1600, 1600, False),),
                               format='JPEG',
                               options={'quality': 80})
    is_featured = models.BooleanField(_('label:is_featured'), default=False)
    is_visible = models.BooleanField(_('label:is_visible'), default=True)
    position = models.PositiveSmallIntegerField(_('label:position'))

    objects = ImageManager()

    class Meta(object):
        verbose_name = _('model:Image')
        verbose_name_plural = _('models:Image')
        ordering = ('position',)
        abstract = True

    def save(self, *args, **kwargs):
        self.hash = hashlib.sha1(str(uuid.uuid1()) + self.file.url).hexdigest()
        super(Image, self).save(*args, **kwargs)

    def get_url(self):
        return self.file.url

    def get_sources(self):
        return get_image_sources(self.IMAGE_TYPE_IN_URL, self.hash) if self.IMAGE_TYPE_IN_URL else None


class XeroxImage(models.Model):
    IMAGE_TYPE_IN_URL = 'x'
    hash = models.CharField(max_length=40, unique=True)
    url = models.URLField(null=True, blank=True)

    class Meta(object):
        db_table = 'core_xerox_image'

    def save(self, *args, **kwargs):
        self.hash = hashlib.sha1(self.url).hexdigest()
        super(XeroxImage, self).save(*args, **kwargs)

    def get_sources(self):
        return get_image_sources(self.IMAGE_TYPE_IN_URL, self.hash)
