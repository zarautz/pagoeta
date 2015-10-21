from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from .models import Place, Type, Image
from pagoeta.apps.core.admin import ImageInline as BaseImageInline


class ImageInline(BaseImageInline):
    model = Image


class PlaceAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'address', 'types_string', 'is_visible')
    list_filter = ('types', 'is_visible')
    search_fields = ('name', 'address', 'email')
    inlines = (ImageInline,)
    raw_id_fields = ('types',)
    autocomplete_lookup_fields = {
        'm2m': ('types',),
    }
    fieldsets = (
        (None, {
            'fields': ('types', 'name', 'description'),
        }),
        (_('fieldset:location'), {
            'fields': ('address', 'latitude', 'longitude'),
        }),
        (_('fieldset:contact_information'), {
            'fields': ('telephone', 'email', 'url'),
        }),
        (_('fieldset:metadata'), {
            'fields': ('is_visible',),
        }),
    )

    def get_queryset(self, request):
        return self.model._default_manager.get_queryset().prefetch_related('types')

    def types_string(self, obj):
        return obj.types_string()
    types_string.short_description = _('models:PlaceType')


class TypeAdmin(TranslationAdmin):
    list_display = ('id', 'code', 'name', 'places_link')
    search_fields = ('code', 'name')
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

    def get_queryset(self, request):
        return self.model._default_manager.get_queryset().extra(select={
            'places_count': 'SELECT COUNT(*) FROM places_place_types WHERE places_place_types.type_id = places_type.id'
        })

    def places_link(self, obj):
        return '<a href="%s">%s</a>' % (
            reverse('admin:places_place_changelist') + '?all=&q=&types__id__exact=' + str(obj.id),
            obj.places_count
        )
    places_link.allow_tags = True
    places_link.short_description = _('models:Place')


admin.site.register(Place, PlaceAdmin)
admin.site.register(Type, TypeAdmin)
