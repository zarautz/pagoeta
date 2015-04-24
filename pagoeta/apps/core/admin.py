from django.contrib import admin


class ImageInline(admin.TabularInline):
    model = None
    exclude = ('hash',)
    extra = 0
    sortable_field_name = 'position'
