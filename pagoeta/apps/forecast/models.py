from django.db import models
from django.utils.translation import ugettext_lazy as _


class WeatherCode(models.Model):
    code = models.CharField('AEMET code', max_length=5)
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name = _('weather code')
        verbose_name_plural = _('weather codes')
        ordering = ('code',)

    def __unicode__(self):
        return u'%s' % self.code
