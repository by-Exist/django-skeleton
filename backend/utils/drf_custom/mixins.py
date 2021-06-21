from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import clone_request


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


# Mixins
# =============================================================================
# List = GET + collection
class ListModelMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            msg = "pagination_class가 지정되지 않았습니다."
            raise Exception(msg)
        paginate_queryset = self.paginator.paginate_queryset(
            queryset, self.request, view=self
        )
        return paginate_queryset


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


# Upsert = PUT + resource (may not be)
# 사용자가 리소스의 pk를 결정할 수 있는 환경이라면 사용한다.
class UpsertModelMixin:
    def update(self, request, *args, **kwargs):
        partial = False
        instance = self.get_object_or_none()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if instance is None:
            assert getattr(
                self, "perform_create", None
            ), "UpsertModelMixin의 생성 동작은 CreateModelMixin을 필요로 합니다."
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Http404:
            self.check_permissions(clone_request(self.request, "POST"))


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
