from django.conf import settings
from django.utils import translation


class LanguageOnQueryParamMiddleware(object):
    def process_request(self, request):
        language = request.GET.get('language', settings.LANGUAGE_CODE)
        translation.activate(language)
        request.LANGUAGE_CODE = language
