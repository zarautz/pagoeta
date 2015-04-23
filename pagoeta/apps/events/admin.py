from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Event, Category, TargetAge, TargetGroup, Image


class ImageInline(admin.TabularInline):
    model = Image
    exclude = ('hash',)
    extra = 0
    sortable_field_name = 'position'


class EventAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'start_at', 'end_at', 'category', 'target_age', 'target_group',
                    'is_visible', 'is_featured')
    list_filter = ('category', 'start_at', 'end_at')
    search_fields = ('name',)
    inlines = (ImageInline,)
    raw_id_fields = ('place',)
    related_lookup_fields = {
        'fk': ('place',),
    }
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'description', 'place'),
        }),
        ('Dates', {
            'fields': ('start_at', 'end_at'),
        }),
        ('More information', {
            'fields': ('url', 'price'),
        }),
        ('Taxonomy', {
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
