from django.db import models
from django.utils.translation import ugettext_lazy as _


class Type(models.Model):
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = _('place type')
        verbose_name_plural = _('place types')
        ordering = ('code',)

    def __unicode__(self):
        return u'%s' % self.name


class Place(models.Model):
    types = models.ManyToManyField(Type, blank=True, related_name='places')
    name = models.CharField(max_length=100)
    description = models.TextField('Presentation', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField('Website', null=True, blank=True)
    price_level = models.CharField(max_length=32, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_visible = models.BooleanField('Visible', default=True)

    class Meta(object):
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __unicode__(self):
        return u'%s' % self.name

    def types_string(self):
        return ', '.join([t.name for t in self.types.all()])
