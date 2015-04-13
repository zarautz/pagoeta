from rest_framework.exceptions import APIException


class ServiceUnavailableException(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
