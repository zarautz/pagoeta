from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Event, Category, TargetAge, TargetGroup, Image
from pagoeta.apps.core.admin import ImageInline as BaseImageInline


class ImageInline(BaseImageInline):
    model = Image


class EventAdmin(TranslationAdmin):
    date_hierarchy = 'start_date'
    list_display = ('id', 'name', 'start_date', 'start_time', 'end_date', 'category', 'target_age', 'target_group',
                    'is_visible', 'is_featured', 'is_superevent')
    list_filter = ('is_superevent', 'category', 'start_date', 'end_date')
    ordering = ('-start_date', '-start_time')
    search_fields = ('name',)
    inlines = (ImageInline,)
    raw_id_fields = ('parent', 'place')
    autocomplete_lookup_fields = {
        'fk': ('parent', 'place'),
    }
    fieldsets = (
        (None, {
            'fields': (('category', 'is_superevent'), 'place', 'parent', 'name', 'description'),
        }),
        (_('fieldset:dates'), {
            'fields': (('start_date', 'end_date'), ('start_time', 'end_time'),
                       ('afternoon_start_time', 'afternoon_end_time'), 'is_all_day_event'),
        }),
        (_('fieldset:more_information'), {
            'fields': ('url', 'price'),
        }),
        (_('fieldset:metadata'), {
            'fields': (('target_age', 'target_group'), 'is_visible', 'is_featured'),
        }),
    )
    actions = ('duplicate_event',)

    def duplicate_event(self, request, queryset):
        """https://docs.djangoproject.com/en/1.7/topics/db/queries/#copying-model-instances"""
        for event in queryset:
            event.id = None
            event.save()

            for image in event.images.all():
                image.id = None
                image.event = event
                image.save()

    duplicate_event.short_description = _('admin_action:duplicate_event')


class TypeAdmin(TranslationAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ('code',)
        else:
            return ()


admin.site.register(Event, EventAdmin)
admin.site.register(Category, TypeAdmin)
admin.site.register(TargetAge, TypeAdmin)
admin.site.register(TargetGroup, TypeAdmin)
