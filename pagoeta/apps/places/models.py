from django.db import models
from hvad.manager import TranslationManager, TranslationQueryset
from hvad.models import TranslatableModel, TranslatedFields


class Type(TranslatableModel):
    code = models.CharField(max_length=32)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
    )

    objects = TranslationManager(default_class=TranslationQueryset)

    def __unicode__(self):
        return u'%s' % self.code


class Place(TranslatableModel):
    types = models.ManyToManyField(Type, blank=True, related_name='places')
    address = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    price_level = models.CharField(max_length=32, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=100),
        description = models.TextField('Presentation', null=True, blank=True),
    )

    objects = TranslationManager(default_class=TranslationQueryset)

    def __unicode__(self):
        return u'%s' % self.address
