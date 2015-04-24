from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.core.models import Image as AbstractImage


class Type(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = _('place type')
        verbose_name_plural = _('place types')
        ordering = ('code',)

    def __unicode__(self):
        return u'%s' % self.name


class PlaceManager(models.Manager):
    def visible(self):
        return self.filter(is_visible=True)


class Place(models.Model):
    types = models.ManyToManyField(Type, blank=True, related_name='places')
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Presentation'), null=True, blank=True)
    address = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    telephone = models.CharField(_('Telephone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('Email'), null=True, blank=True)
    url = models.URLField(_('Website'), null=True, blank=True)
    price_level = models.CharField(max_length=32, null=True, blank=True)
    latitude = models.DecimalField(max_digits=18, decimal_places=12, null=True, blank=True)
    longitude = models.DecimalField(max_digits=18, decimal_places=12, null=True, blank=True)
    is_visible = models.BooleanField(_('Visible'), default=True)

    objects = PlaceManager()

    class Meta(object):
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __unicode__(self):
        return u'%s' % self.name

    def types_string(self):
        return ', '.join([t.name for t in self.types.all()])

    def image(self):
        if self.images.count() > 0:
            return self.images.all()[0]
        else:
            return None


class Image(AbstractImage):
    IMAGE_TYPE_IN_URL = 'p'
    place = models.ForeignKey(Place, null=True, blank=True, related_name='images')

    def get_asset_directory(self):
        return 'public/places'
