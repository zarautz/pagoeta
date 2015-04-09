from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import translation


class AnonymousSessionMiddleware(SessionMiddleware):
    """
    This middleware extends the Django SessionMiddleware removing
    the cookie (if set) for anonymous users and setiing a default
    'Cache-Control' header for all responses.
    """
    def process_response(self, request, response):
        response = super(AnonymousSessionMiddleware, self).process_response(request, response)
        if not request.user.is_authenticated():
            if settings.SESSION_COOKIE_NAME in request.COOKIES:
                response.delete_cookie(settings.SESSION_COOKIE_NAME)
            if not 'Cache-Control' in response:
                max_age = getattr(settings, 'CACHE_CONTROL_MAX_AGE', 300)
                response['Cache-Control'] = 'public, max-age=%d, s-maxage=%d' % (max_age, max_age)
        return response


class LanguageOnQueryParamMiddleware(object):
    def process_request(self, request):
        language = request.GET.get('language', settings.LANGUAGE_CODE)
        translation.activate(language)
        request.LANGUAGE_CODE = language
