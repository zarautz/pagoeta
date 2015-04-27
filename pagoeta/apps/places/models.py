from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.core.models import Image as AbstractImage


class Type(models.Model):
    code = models.CharField(_('label:code'), max_length=32)
    name = models.CharField(_('label:name'), max_length=255)

    class Meta(object):
        verbose_name = _('model:PlaceType')
        verbose_name_plural = _('models:PlaceType')
        ordering = ('name',)

    def __unicode__(self):
        return u'%s' % self.name


class PlaceManager(models.Manager):
    def visible(self):
        return self.filter(is_visible=True)


class Place(models.Model):
    types = models.ManyToManyField(Type, blank=True, related_name='places', verbose_name=_('models:PlaceType'))
    name = models.CharField(_('label:name'), max_length=100)
    description = models.TextField(_('label:description'), null=True, blank=True)
    address = models.CharField(_('label:address'), max_length=255, null=True, blank=True)
    telephone = models.CharField(_('label:telephone'), max_length=32, null=True, blank=True)
    email = models.EmailField(_('label:email'), null=True, blank=True)
    url = models.URLField(_('label:url'), null=True, blank=True)
    price_level = models.PositiveSmallIntegerField(_('label:price_level'), null=True, blank=True)
    latitude = models.DecimalField(_('label:latitude'), max_digits=18, decimal_places=12, null=True, blank=True)
    longitude = models.DecimalField(_('label:longitude'), max_digits=18, decimal_places=12, null=True, blank=True)
    is_visible = models.BooleanField(_('label:is_visible'), default=True)

    objects = PlaceManager()

    class Meta(object):
        verbose_name = _('model:Place')
        verbose_name_plural = _('models:Place')

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
