from django.db import models

from pagoeta.apps.places.models import Place


class Pharmacy(models.Model):
    cofg_id = models.PositiveSmallIntegerField('COFG id', unique=True)
    place = models.ForeignKey(Place, related_name='pharmacy')
