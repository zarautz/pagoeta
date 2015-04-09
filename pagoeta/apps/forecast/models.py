from django.db import models
from hvad.manager import TranslationManager, TranslationQueryset
from hvad.models import TranslatableModel, TranslatedFields


class WeatherCode(TranslatableModel):
    code = models.CharField(max_length=5)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
    )

    objects = TranslationManager(default_class=TranslationQueryset)

    def __unicode__(self):
        return u'%s' % self.code
