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
#               HTTP Mapping        HTTP request body       HTTP response body
# List          GET + collection    X                       resource list
# Retrieve      GET + resource      X                       resource
# Create        POST + collection   resource data           resource
# Replace       PUT + resource      resource data           resource
# Modify        PATCH + resource    resource partial data   resource
# Delete        DELETE + resource   X                       X


# PUT과 PATCH의 차이에 대한 이해
# =============================================================================
# PUT
#   - url을 통해 생성될 자원의 식별자를 클라이언트가 지정할 수 있다
#   - 해당 위치에 이미 자원이 없다면 생성, 있다면 교체한다
#   - "???"
# PATCH
#   - url의 위치에 리소스가 이미 존재한다는 걸 가정한다
#   - 해당 위치에 있는 자원을 수정한다
#   - "modify"


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
            and request.query_params.get("validate_only", None) == "1"
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


# Retrieve = GET + resource
from rest_framework.mixins import RetrieveModelMixin

# Create = POST + collection
from rest_framework.mixins import CreateModelMixin

# Replace = PUT + resource (may not be)
class ReplaceModelMixin:
    def replace(self, request, *args, **kwargs):
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_replace(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_replace(self, serializer):
        serializer.save()


# TODO: ReplaceOrCreateModelMixin 정의


# Modify = PATCH + resource
class ModifyModelMixin:
    def modify(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_modify(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_modify(self, serializer):
        serializer.save()


# Destroy = DELETE + resource
from rest_framework.mixins import DestroyModelMixin
