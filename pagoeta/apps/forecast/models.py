from django.db import models
from django.utils.translation import ugettext_lazy as _


class WeatherCode(models.Model):
    code = models.CharField(_('label:aemet_code'), max_length=5)
    name = models.CharField(_('label:name'), max_length=255)

    class Meta(object):
        verbose_name = _('model:WeatherCode')
        verbose_name_plural = _('models:WeatherCode')
        ordering = ('code',)

    def __unicode__(self):
        return u'%s' % self.code
