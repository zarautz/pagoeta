from django.db import models
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.places.models import Place


class Type(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta(object):
        abstract = True

    def __unicode__(self):
        return u'%s' % self.name


class Category(Type):
    class Meta(object):
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('name',)


class TargetAge(Type):
    class Meta(object):
        verbose_name = _('target age group')
        verbose_name_plural = _('target age groups')


class TargetGroup(Type):
    class Meta(object):
        verbose_name = _('target group')
        verbose_name_plural = _('target groups')


class EventManager(models.Manager):
    def visible(self):
        return self.filter(is_visible=True)


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    place = models.ForeignKey(Place, related_name='events')
    category = models.ForeignKey(Category, related_name='events')
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subevents')
    target_group = models.ForeignKey(TargetGroup, related_name='events')
    target_age = models.ForeignKey(TargetAge, related_name='events')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_featured = models.BooleanField('Featured', default=False)
    is_visible = models.BooleanField('Visible', default=True)

    is_superevent = models.BooleanField('Visible', default=True)

    objects = EventManager()

    class Meta(object):
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __unicode__(self):
        return u'%s' % self.name
