from modeltranslation.translator import translator, TranslationOptions

from .models import Place, Type


class PlaceTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class TypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Place, PlaceTranslationOptions)
translator.register(Type, TypeTranslationOptions)
