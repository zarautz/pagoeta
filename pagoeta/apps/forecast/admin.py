from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import WeatherCode


class WeatherCodeAdmin(TranslationAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ('code',)
        else:
            return ()


admin.site.register(WeatherCode, WeatherCodeAdmin)
