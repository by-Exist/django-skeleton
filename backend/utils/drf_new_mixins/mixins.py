from rest_framework import mixins as rest_mixins
from rest_framework.response import Response
from .exceptions import PaginatorNotFound
from .serializers import ValidateOnlySerializerMixin


# 부작용, 멱등성
# =============================================================================
# 부작용(not safe) = 데이터를 변경시키는가
# 멱등성 = 동일한 요청 형식이라면 몇 번을 하더라도 동일한 결과를 보장하는가
# 멱등 O, 부작용 X = ["GET", "HEAD", "OPTION", "TRACE"]
# 멱등 O, 부작용 O = ["PUT", "DELETE"]
# 멱등 X, 부작용 O = ["POST", "PATCH"]


# 표준 메서드
# =============================================================================
#                   HTTP Mapping        HTTP request body       HTTP response body
# List              GET + collection    X                       resource list
# Retrieve          GET + resource      X                       resource
# Create            POST + collection   resource data           resource
# Update            PUT + resource      resource data           resource
# Upsert            PUT + resource      resource data           resource
# Partial Update    PATCH + resource    resource partial data   resource
# Delete            DELETE + resource   X                       X
#
# Update, 기존 자원이 있어야만 하는 경우
# Upsert, 기존 자원이 없을 때 생성까지 해주는 경우


# Util Mixins
# =============================================================================
class RequiredPaginationMixin:
    def paginate_queryset(self, queryset):
        if self.paginator is None:
            msg = "paginator를 찾을 수 없습니다. pagination_class가 지정되었는지 확인하세요."
            raise PaginatorNotFound(msg)
        return self.paginator.paginate_queryset(queryset, self.request, view=self)


class ValidateOnlyViewSetMixin:
    validate_only_param = "validate_only"
    validate_only_actions = []
    allow_validate_only_http_methods = ["POST", "PUT", "PATCH"]

    def initialize_request(self, request, *args, **kwargs):
        # validate only 기능의 활성화 여부를 request.validate_only에 기록한다.
        request = super().initialize_request(request, *args, **kwargs)
        if (
            self.action in self.validate_only_actions
            and request.method in self.allow_validate_only_http_methods
            and request.query_params.get("validate_only", None) == "true"
        ):
            request.validate_only = True
        else:
            request.validate_only = False
        return request

    def get_serializer_class(self):
        # validate_only 기능이 활성화 되었을 때 사용되는 시리얼라이저가
        # ValidateOnlySerializerMixin을 상속해야 함을 명시한다.
        serializer_class = super().get_serializer_class()
        if self.request.validate_only and not issubclass(
            serializer_class, ValidateOnlySerializerMixin
        ):
            msg = (
                "validate only 기능을 활용하기 위해서는 {}가"
                "ValidateOnlySerializerMixin을 상속해야 합니다."
            ).format(serializer_class.__name__)
            raise AssertionError(msg)
        return serializer_class


# Mixins
# =============================================================================
# List = GET + collection
class ListModelMixin(RequiredPaginationMixin, rest_mixins.ListModelMixin):
    pass


# Create = POST + collection
from rest_framework.mixins import CreateModelMixin


# Retrieve = GET + resource
from rest_framework.mixins import RetrieveModelMixin


# Update = PUT + resource (required)
class UpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


# TODO: Upsert 구현, 메서드 이름은 유지해야 한다!
# # Upsert = PUT + resource (may not be)
# class UpsertModelMixin:
#     def update(self, request, *args, **kwargs):
#         partial = False
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         if getattr(instance, "_prefetched_objects_cache", None):
#             instance._prefetched_objects_cache = {}
#         return Response(serializer.data)

#     def perform_update(self, serializer):
#         serializer.save()


# Partial Update = PATCH + resource
class PartialUpdateModelMixin:
    def partial_update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_partial_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_partial_update(self, serializer):
        serializer.save()


# Destroy = DELETE + resource
from rest_framework.mixins import DestroyModelMixin
