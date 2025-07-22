from __future__ import unicode_literals
from django.db import IntegrityError



from rest_framework import status
from rest_framework.views import Response, exception_handler
from rest_framework.exceptions import APIException
from django.utils.encoding import force_str


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    # if there is an IntegrityError and the error response hasn't already been generated
    # if isinstance(exc, IntegrityError) and not response:
    #     response = Response(
    #         {
    #             'message': 'IntegrityError'
    #         },
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
    #     sentry_sdk.capture_exception(exc)

    return response


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else: self.detail = {'detail': force_str(self.default_detail)}