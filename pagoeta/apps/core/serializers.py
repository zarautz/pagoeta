from django.conf import settings
from rest_framework import serializers


class TranslationModelSerializer(serializers.ModelSerializer):
    """
    This serializer excludes by default translation specific fields.
    When using the serializer you need to set a `Meta.translation_fields` attribute.
    """
    def __init__(self, *args, **kwargs):
        super(TranslationModelSerializer, self).__init__(*args, **kwargs)
        self.translation_fields = getattr(self.Meta, 'translation_fields', ())

        for language in settings.LANGUAGES:
            for field in self.translation_fields:
                key = field + '_' + language[0]
                if self.fields.get(key):
                    self.fields.pop(key)
