from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, views as rest_views, status
from rest_framework.response import Response
from .exceptions import PerformValidateOnly


def exception_handler(exc, context):

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"detail": exc.detail}
        rest_views.set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    # is_valid 시 raise_exception이 True라서 PerformValidateOnly이 발생한 경우
    # return Response(status=status.HTTP_204_NO_CONTENT)
    if isinstance(exc, PerformValidateOnly):
        return Response(status=status.HTTP_204_NO_CONTENT)

    return None
