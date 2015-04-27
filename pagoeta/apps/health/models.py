from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.places.models import Place


class Pharmacy(models.Model):
    cofg_id = models.PositiveSmallIntegerField(_('label:cofg_id'), unique=True)
    place = models.ForeignKey(Place, related_name='pharmacy', verbose_name=_('model:Place'))

    class Meta(object):
        verbose_name = _('model:Pharmacy')
        verbose_name_plural = _('models:Pharmacies')

    def __unicode__(self):
        return u'%s' % self.place.name
