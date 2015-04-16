from modeltranslation.translator import translator, TranslationOptions

from .models import Event, Category, TargetAge, TargetGroup


class EventTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class TypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Event, EventTranslationOptions)
translator.register(Category, TypeTranslationOptions)
translator.register(TargetAge, TypeTranslationOptions)
translator.register(TargetGroup, TypeTranslationOptions)
