from modeltranslation.translator import translator, TranslationOptions

from .models import WeatherCode


class WeatherCodeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(WeatherCode, WeatherCodeTranslationOptions)
