from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from utils.drf_custom import mixins
from utils.drf_custom.viewsets import GenericViewSet
from utils.drf_custom.filters import (
    OrderingFilterBackend,
    BatchGetFilterBackend,
    PathVariableFilterBackend,
)
from utils.drf_custom.filterset import DjangoFilterBackend
from utils.drf_custom.pagination import SmallPageNumberPagination
from .filters import CollectionFilter
from .models import Collection, NestedCollection, NestedResource
from .serializers import (
    CollectionSerializer,
    NestedCollectionSerializer,
    MoveNestedCollectionSerializer,
    NestedResourceSerializer,
)


class CollectionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    # Attributes
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    validate_only_actions = ["create", "partial_update"]

    @property
    def filter_backends(self):
        map = {
            "list": [OrderingFilterBackend],
            "batch_get": [OrderingFilterBackend, BatchGetFilterBackend],
            "search": [OrderingFilterBackend, DjangoFilterBackend],
        }
        if self.action in map:
            return map[self.action]
        return []

    ordering_fields = ["id", "title"]
    batch_get_value_regex = "^[0-9]+$"
    filterset_class = CollectionFilter

    pagination_class = SmallPageNumberPagination

    # Actions
    @action(methods=["get"], detail=False, url_path="batchGet")
    def batch_get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=["get"], detail=False)
    def search(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        obj = serializer.save()
        NestedResource.objects.create(parent=obj, title=f"{obj.pk}의 중첩된 리소스")


class NestedCollectionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    # Attributes
    path_variable_config = {
        "collection_pk": {
            "field": "parent",
            "allow_wildcard_actions": ["list", "retrieve"],
        }
    }

    queryset = NestedCollection.objects.all().select_related("parent")

    @property
    def serializer_class(self):
        if self.action == "move":
            return MoveNestedCollectionSerializer
        return NestedCollectionSerializer

    validate_only_actions = ["create", "partial_update"]

    @property
    def filter_backends(self):
        map = {
            "list": [OrderingFilterBackend, PathVariableFilterBackend],
            "retrieve": [PathVariableFilterBackend],
        }
        if self.action in map:
            return map[self.action]
        return []

    ordering_fields = ["id", "title"]

    pagination_class = SmallPageNumberPagination

    # Actions
    @action(methods=["post"], detail=True)
    def move(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_create(self, serializer):
        parent = get_object_or_404(Collection, pk=self.kwargs["collection_pk"])
        return serializer.save(parent=parent)


class NestedResourceViewSet(
    mixins.RetrieveModelMixin, mixins.PartialUpdateModelMixin, GenericViewSet,
):
    # Attributes
    lookup_field = "parent__pk"
    lookup_url_kwarg = "collection_pk"

    queryset = NestedResource.objects.all().select_related("parent")
    serializer_class = NestedResourceSerializer

    validate_only_actions = ["partial_update"]
