from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from pagoeta.apps.core.models import Image as AbstractImage
from pagoeta.apps.places.models import Place


class Type(models.Model):
    code = models.CharField(_('label:code'), max_length=100)
    name = models.CharField(_('label:name'), max_length=255)

    class Meta(object):
        abstract = True

    def __unicode__(self):
        return u'%s' % self.name


class Category(Type):
    class Meta(object):
        verbose_name = _('model:Category')
        verbose_name_plural = _('models:Category')
        ordering = ('name',)


class TargetAge(Type):
    class Meta(object):
        verbose_name = _('model:TargetAge')
        verbose_name_plural = _('models:TargetAge')
        ordering = ('id',)


class TargetGroup(Type):
    class Meta(object):
        verbose_name = _('model:TargetGroup')
        verbose_name_plural = _('models:TargetGroup')
        ordering = ('id',)


class EventManager(models.Manager):
    def visible(self):
        return self.filter(is_visible=True)


class Event(models.Model):
    name = models.CharField(_('label:name'), max_length=255)
    description = models.TextField(_('label:description'))
    place = models.ForeignKey(Place, related_name='events', null=True, blank=True, verbose_name=_('model:Place'))
    category = models.ForeignKey(Category, related_name='events', verbose_name=_('model:Category'))
    target_group = models.ForeignKey(TargetGroup, related_name='events', null=True, blank=True,
                                     verbose_name=_('model:TargetGroup'))
    target_age = models.ForeignKey(TargetAge, related_name='events', null=True, blank=True,
                                   verbose_name=_('model:TargetAge'))
    start_date = models.DateField(_('label:start_date'))
    end_date = models.DateField(_('label:end_date'), null=True, blank=True)
    start_time = models.TimeField(_('label:start_time'), null=True, blank=True)
    end_time = models.TimeField(_('label:end_time'), null=True, blank=True, help_text=_('help_text:end_time'))
    afternoon_start_time = models.TimeField(_('label:afternoon_start_time'), null=True, blank=True)
    afternoon_end_time = models.TimeField(_('label:afternoon_end_time'), null=True, blank=True,
                                          help_text=_('help_text:afternoon_end_time'))
    is_all_day_event = models.BooleanField(_('label:is_all_day_event'), default=False,
                                           help_text=_('help_text:is_all_day_event'))
    price = models.DecimalField(_('label:price'), max_digits=6, decimal_places=2, null=True, blank=True)
    url = models.URLField(_('label:url'), null=True, blank=True)
    is_featured = models.BooleanField(_('label:is_featured'), default=False)
    is_superevent = models.BooleanField(_('label:is_superevent'), default=False,
                                        help_text=_('help_text:is_superevent'))
    is_visible = models.BooleanField(_('label:is_visible'), default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subevents',
                               limit_choices_to={'is_superevent': True},
                               verbose_name=_('label:parent_superevent'), help_text=_('help_text:parent_superevent'))

    objects = EventManager()

    class Meta(object):
        verbose_name = _('model:Event')
        verbose_name_plural = _('models:Event')
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
