from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Event, Category, TargetAge, TargetGroup, Image
from pagoeta.apps.core.admin import ImageInline as BaseImageInline


class ImageInline(BaseImageInline):
    model = Image


class EventAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'start_date', 'start_time', 'end_date', 'category', 'target_age', 'target_group',
                    'is_visible', 'is_featured')
    list_filter = ('category', 'start_date', 'end_date')
    search_fields = ('name',)
    inlines = (ImageInline,)
    raw_id_fields = ('parent', 'place')
    related_lookup_fields = {
        'fk': ('parent', 'place'),
    }
    fieldsets = (
        (None, {
            'fields': ('category', 'place', ('parent', 'is_superevent'), 'name', 'description'),
        }),
        ('Dates', {
            'fields': (('start_date', 'end_date'), ('start_time', 'end_time'),
                       ('afternoon_start_time', 'afternoon_end_time'), 'is_all_day_event'),
        }),
        ('More information', {
            'fields': ('url', 'price'),
        }),
        ('Metadata', {
            'fields': (('target_age', 'target_group'), 'is_visible', 'is_featured'),
        }),
    )


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
