from ratelimit.exceptions import Ratelimited
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exec, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = drf_exception_handler(exec, context)

    # Now add the HTTP status code to the response.
    if isinstance(exec, Ratelimited):
        response.data['detail'] = 'Too many requests, try again later.'
        response.status_code = 429

    return response
