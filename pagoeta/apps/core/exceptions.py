from rest_framework.exceptions import APIException
from rest_framework import status


class ServiceUnavailableException(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporarily unavailable, try again later.'
