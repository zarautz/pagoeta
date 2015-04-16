from django.contrib import admin

from .models import WeatherCode


class WeatherCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ('code',)
        else:
            return ()


admin.site.register(WeatherCode, WeatherCodeAdmin)
