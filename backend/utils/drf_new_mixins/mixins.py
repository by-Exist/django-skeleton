from rest_framework.response import Response


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
# List = GET + collection uri
from rest_framework.mixins import ListModelMixin

# Retrieve = GET + resource uri
from rest_framework.mixins import RetrieveModelMixin

# Create = POST + collection uri
from rest_framework.mixins import CreateModelMixin

# Replace = PUT + resource uri
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


# Modify = PATCH + resource uri
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


# Destroy = DELETE + resource uri
from rest_framework.mixins import DestroyModelMixin
