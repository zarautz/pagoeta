from django.db import models
from hvad.manager import TranslationManager, TranslationQueryset
from hvad.models import TranslatableModel, TranslatedFields

from pagoeta.apps.places.models import Place


class Type(TranslatableModel):
    code = models.CharField(max_length=100)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
    )

    objects = TranslationManager(default_class=TranslationQueryset)

    class Meta(object):
        abstract = True

    def __unicode__(self):
        return u'%s' % self.code


class Category(Type):
    translations = TranslatedFields()


class TargetGroup(Type):
    translations = TranslatedFields()


class TargetAge(Type):
    translations = TranslatedFields()


class Event(TranslatableModel):
    place = models.ForeignKey(Place, related_name='events')
    category = models.ForeignKey(Category, related_name='events')
    target_group = models.ForeignKey(TargetGroup, related_name='events')
    target_age = models.ForeignKey(TargetAge, related_name='events')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    price = models.PositiveSmallIntegerField()
    url = models.URLField(null=True, blank=True)
    is_featured = models.BooleanField('Featured', default=False)
    is_visible = models.BooleanField('Visible', default=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        description = models.TextField(),
    )

    objects = TranslationManager(default_class=TranslationQueryset)

    def __unicode__(self):
        return u'%s' % self.name
