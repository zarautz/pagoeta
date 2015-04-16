from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.places.models import Place


class Pharmacy(models.Model):
    cofg_id = models.PositiveSmallIntegerField('COFG id', unique=True)
    place = models.ForeignKey(Place, related_name='pharmacy')

    class Meta(object):
        verbose_name = _('pharmacy')
        verbose_name_plural = _('pharmacies')

    def __unicode__(self):
        return u'%s' % self.place.name
