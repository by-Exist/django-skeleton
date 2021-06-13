from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.serializers import BooleanField


# 부작용, 멱등성
# =============================================================================
# 부작용(not safe) = 데이터를 변경시키는가
# 멱등성 = 동일한 요청 형식이라면 몇 번을 하더라도 동일한 결과를 보장하는가
# 멱등 O, 부작용 X = ["GET", "HEAD", "OPTION", "TRACE"]
# 멱등 O, 부작용 O = ["PUT", "DELETE"]
# 멱등 X, 부작용 O = ["POST", "PATCH"]


# 표준 메서드
# =============================================================================
#               HTTP Mapping        HTTP request body       HTTP response body
# List          GET + collection    X                       resource list
# Retrieve      GET + resource      X                       resource
# Create        POST + collection   resource data           resource
# Replace       PUT + resource      resource data           resource
# Modify        PATCH + resource    resource partial data   resource
# Delete        DELETE + resource   X                       X


# Custom Mixins
# =============================================================================
# List = GET HTTP method + collection uri
class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# Create = POST HTTP method + collection uri
class CreateModelMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # here
        if serializer.validated_data.pop("validate_only", False):
            return Response(status=status.HTTP_200_OK)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


# Retrieve = GET HTTP method + resource uri
from rest_framework.mixins import RetrieveModelMixin


# Replace = PUT HTTP method + resource uri
class ReplaceModelMixin:
    def replace(self, request, *args, **kwargs):
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # here
        if serializer.validated_data.pop("validate_only", False):
            return Response(status=status.HTTP_200_OK)

        self.perform_replace(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_replace(self, serializer):
        serializer.save()


# Modify = PATCH HTTP method + resource uri
class ModifyModelMixin:
    def modify(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # here
        if serializer.validated_data.pop("validate_only", False):
            return Response(status=status.HTTP_200_OK)

        self.perform_modify(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_modify(self, serializer):
        serializer.save()


# Destroy = DELETE HTTP method + resource uri
from rest_framework.mixins import DestroyModelMixin


# Util Mixins
# =============================================================================
class CheckPageableMixin:
    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                raise AssertionError("뷰에 pagination_class가 지정되지 않았습니다.")
            else:
                self._paginator = self.pagination_class()
        assert (
            self._paginator.page_size
        ), "page_size가 지정되어 있지 않습니다. pagination_class에 page_size가 지정되지 않았거나 api_settings.PAGE_SIZE가 설정되지 않았습니다."
        return self._paginator


class AddValidateOnlyFieldMixin:

    validate_only_actions = []
    allow_validate_only_methods = ["POST", "PUT", "PATCH"]

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        if self.action not in self.validate_only_actions:
            return serializer

        assert (
            self.method in self.allow_validate_only_methods
        ), "validate_only 기능은 body를 사용할 수 있는 http request ({})에서만 사용할 수 있습니다. ".format(
            self.action, ", ".join(self.allow_validate_only_methods)
        )

        validate_only_field = BooleanField(
            write_only=True, required=False, help_text="필드의 유효성 검사만을 수행합니다.",
        )
        serializer.fields["validate_only"] = validate_only_field

        return serializer
