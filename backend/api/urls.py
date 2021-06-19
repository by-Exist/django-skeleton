from django.urls import register_converter
from utils.drf_new_mixins import routers
from apps.example.views import (
    CollectionViewSet,
    NestedCollectionViewSet,
    NestedResourceViewSet,
)
from .converters import VersionConverter


# API Setting
# =============================================================================
API_VERSION = "v1"
register_converter(VersionConverter, "version")


# Router
# =============================================================================
collections_router = routers.CustomSimpleRouter()
collections_router.trailing_slash = "/?"
collections_router.register("collections", CollectionViewSet, basename="collection")

nested_collections_router = routers.CustomNestedSimpleRouter(
    collections_router, "collections"
)
nested_collections_router.register(
    "nested-collections", NestedCollectionViewSet, basename="nested-collection"
)

nested_resource_router = routers.NestedSingletonSimpleRouter(
    collections_router, "collections"
)
nested_resource_router.register(
    "nested-singleton", NestedResourceViewSet, basename="nested-resource"
)


# API URL Build
# =============================================================================
urlpatterns = [
    *collections_router.urls,
    *nested_collections_router.urls,
    *nested_resource_router.urls,
]


# Load Drf Spectacular Schemas
# =============================================================================
from .schema import *
