from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Place, Type, Image


class ImageInline(admin.TabularInline):
    model = Image
    exclude = ('hash',)
    extra = 0
    sortable_field_name = 'position'


class PlaceAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'address', 'types_string', 'is_visible')
    list_filter = ('types', 'is_visible')
    search_fields = ('name', 'address', 'email')
    inlines = (ImageInline,)
    raw_id_fields = ('types',)
    related_lookup_fields = {
        'm2m': ('types',),
    }
    fieldsets = (
        (None, {
            'fields': ('types', 'name', 'description'),
        }),
        ('Location', {
            'fields': ('address', 'latitude', 'longitude'),
        }),
        ('Contact information', {
            'fields': ('telephone', 'email', 'url'),
        }),
    )


class TypeAdmin(TranslationAdmin):
    list_display = ('id', 'code', 'name')
    fieldsets = (
        (None, {
            'fields': ('code', 'name'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ('code',)
        else:
            return ()


admin.site.register(Place, PlaceAdmin)
admin.site.register(Type, TypeAdmin)
