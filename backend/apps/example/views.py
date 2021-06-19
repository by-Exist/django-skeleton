from utils.drf_new_mixins import mixins
from utils.drf_new_mixins.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema
from .models import Collection, NestedCollection, NestedResource
from .serializers import (
    CollectionSerializer,
    NestedCollectionSerializer,
    NestedResourceSerializer,
)


@extend_schema(tags=["collection"])
class CollectionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


@extend_schema(tags=["nested-collection"])
class NestedCollectionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = NestedCollection.objects.all()
    serializer_class = NestedCollectionSerializer


@extend_schema(tags=["nested-resource"])
class NestedResourceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = NestedResource.objects.all()
    serializer_class = NestedResourceSerializer
