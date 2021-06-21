from django.urls import register_converter
from utils.drf_custom import routers
from apps.example import views
from .converters import VersionConverter


# API Setting
# =============================================================================
register_converter(VersionConverter, "version")


# Router
# =============================================================================
collections_router = routers.CustomSimpleRouter()
collections_router.trailing_slash = "/?"
collections_router.register(
    "collections", views.CollectionViewSet, basename="collection"
)
nested_collections_router = routers.CustomNestedSimpleRouter(
    collections_router, "collections", lookup="collection"
)
nested_collections_router.register(
    "nested-collections", views.NestedCollectionViewSet, basename="nested-collection",
)
nested_resource_router = routers.NestedSingletonSimpleRouter(
    collections_router, "collections", lookup="collection"
)
nested_resource_router.register(
    "nested-singleton", views.NestedResourceViewSet, basename="nested-resource"
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
