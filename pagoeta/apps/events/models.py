from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.core.models import Image as AbstractImage
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
    place = models.ForeignKey(Place, related_name='events', null=True, blank=True)
    category = models.ForeignKey(Category, related_name='events')
    target_group = models.ForeignKey(TargetGroup, related_name='events', null=True, blank=True)
    target_age = models.ForeignKey(TargetAge, related_name='events', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True,
                                help_text=_('This time will be the morning end time if afternoon times are set.'))
    afternoon_start_time = models.TimeField(null=True, blank=True)
    afternoon_end_time = models.TimeField(null=True, blank=True,
                                          help_text=_('Afternoon times are only needed is the hours are split.'))
    is_all_day_event = models.BooleanField(_('All day event'), default=False,
                                           help_text=_('Check this if it is an all day event (no hours).'))
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_superevent = models.BooleanField(_('Super event'), default=False,
                                        help_text=_('Check this if this event can have children events.'))
    is_visible = models.BooleanField(_('Visible'), default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subevents',
                               limit_choices_to={'is_superevent': True},
                               help_text=_('Select one if this event is part of a super event.'))

    objects = EventManager()

    class Meta(object):
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('start_date', 'start_time')

    def clean(self):
        """
        Validates the model before saving.
        """
        # 1) Check if it is a superevent with a parent event defined
        if self.is_superevent and self.parent:
            raise ValidationError(_('A super event cannot have a parent event.'))
        # 2) Check if the necessary dates and times are defined
        if not self.is_all_day_event:
            if not self.end_date:
                self.end_date = self.start_date
            if not self.start_time:
                raise ValidationError(_('A start time is required if the event is not an all day event.'))
            if (self.afternoon_start_time or self.afternoon_end_time) and not self.end_time:
                raise ValidationError(_('Make sure you set the morning end time if you are setting afternoon times.'))
        else:
            self.start_time, self.end_time, self.afternoon_start_time, self.afternoon_end_time = None, None, None, None

    def __unicode__(self):
        return u'%s' % self.name

    def image(self):
        if self.images.count() > 0:
            return self.images.all()[0]
        else:
            return None

    @cached_property
    def start_at(self):
        start_time = self.start_time if self.start_time else datetime.min.time()
        return datetime.combine(self.start_date, start_time)

    @cached_property
    def end_at(self):
        end_time = self.afternoon_end_time if self.afternoon_end_time else self.end_time
        return datetime.combine(self.end_date, end_time) if end_time else None


class Image(AbstractImage):
    IMAGE_TYPE_IN_URL = 'e'
    event = models.ForeignKey(Event, null=True, blank=True, related_name='images')

    def get_asset_directory(self):
        return 'public/events'
