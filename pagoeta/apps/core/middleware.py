from django.conf import settings
from django.http import JsonResponse
from django.utils import translation
from rest_framework import status


class LanguageOnQueryParamMiddleware(object):
    def process_request(self, request):
        if request.path.startswith('/admin'):
            language = settings.LANGUAGE_CODE
        else:
            language = request.GET.get('language', settings.LANGUAGE_CODE)
            if language != settings.LANGUAGE_CODE:
                available_languages = [l[0] for l in settings.LANGUAGES]
                if language not in available_languages:
                    return JsonResponse({'detail': 'Language has to be one of: %s.' % ', '.join(available_languages)},
                                        status=status.HTTP_400_BAD_REQUEST)

        translation.activate(language)
        request.LANGUAGE_CODE = language
