from django.contrib import admin

from .models import Pharmacy


class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'cofg_id', 'place')
    raw_id_fields = ('place',)
    autocomplete_lookup_fields = {
        'fk': ('place',),
    }
    fieldsets = (
        (None, {
            'fields': ('cofg_id', 'place'),
        }),
    )


admin.site.register(Pharmacy, PharmacyAdmin)
