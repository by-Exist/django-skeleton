from django.shortcuts import get_object_or_404
from utils.drf_custom import mixins
from utils.drf_custom.decorators import action
from utils.drf_custom.viewsets import GenericViewSet
from utils.drf_custom.filters import (
    OrderingFilterBackend,
    BatchGetFilterBackend,
    DjangoFilterBackend,
)
from utils.drf_custom.pagination import SmallPageNumberPagination
from .models import Collection, NestedCollection, NestedResource
from .serializers import (
    CollectionSerializer,
    NestedCollectionSerializer,
    MoveNestedCollectionSerializer,
    NestedResourceSerializer,
)
from .filters import CollectionFilter


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

    filter_backends_map = {
        "list": [OrderingFilterBackend],
        "batch_get": [OrderingFilterBackend, BatchGetFilterBackend],
        "search": [OrderingFilterBackend, DjangoFilterBackend],
    }
    ordering_fields = ["id", "title"]
    batch_get_value_regex = "^[0-9]+$"
    filterset_class = CollectionFilter

    pagination_class = SmallPageNumberPagination

    validate_only_actions = ["create", "partial_update"]

    # Actions
    @action(
        methods=["get"], detail=False, custom_method=True,
    )
    def batch_get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(
        methods=["get"], detail=False, custom_method=True,
    )
    def search(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # Overwrite Methods
    def filter_queryset(self, queryset):
        for backend in self.filter_backends_map[self.action]:
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

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
    queryset = NestedCollection.objects.all().select_related("parent")
    serializer_class = NestedCollectionSerializer

    pagination_class = SmallPageNumberPagination

    # Actions
    @action(
        methods=["post"], detail=True, custom_method=True,
    )
    def move(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # Overwrite Methods
    def get_queryset(self):
        qs = super().get_queryset()
        collection_pk_value: str = self.kwargs["collection_pk"]
        try:
            collection_pk = int(collection_pk_value)
            qs = qs.filter(parent__pk=collection_pk)
        except:
            pass
        return qs

    def get_serializer_class(self):
        if self.action == "move":
            return MoveNestedCollectionSerializer
        return super().get_serializer_class()

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
