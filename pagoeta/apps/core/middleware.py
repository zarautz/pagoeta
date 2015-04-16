from django.conf import settings
from django.utils import translation


class LanguageOnQueryParamMiddleware(object):
    def process_request(self, request):
        if request.path.startswith('/admin'):
            language = settings.LANGUAGE_CODE
        else:
            language = request.GET.get('language', settings.LANGUAGE_CODE)

        translation.activate(language)
        request.LANGUAGE_CODE = language
