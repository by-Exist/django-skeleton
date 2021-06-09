from django.urls import register_converter
from utils.drf_custom_method.routers import (
    CustomMethodSimpleRouter,
    NestedCustomMethodSimpleRouter,
    NestedSingletonResourceCustomMethodSimpleRouter,
)
from apps.exampleapp.views import (
    UserViewSet,
    PostViewSet,
    GroupViewSet,
    UserSettingViewSet,
)
from .converters import VersionConverter


# API Version
# =============================================================================
API_VERSION = "v1"


# Set Converters
# =============================================================================
register_converter(VersionConverter, "version")


# Router
# =============================================================================
router = CustomMethodSimpleRouter()
router.trailing_slash = "/?"
router.register("users", UserViewSet, basename="user")
router.register("posts", PostViewSet, basename="post")
router.register("groups", GroupViewSet, basename="group")

users_nested_router = NestedCustomMethodSimpleRouter(router, "users", lookup="user")
users_nested_router.trailing_slash = "/?"

users_nested_singleton_router = NestedSingletonResourceCustomMethodSimpleRouter(
    router, "users", lookup="user"
)
users_nested_singleton_router.trailing_slash = "/?"
users_nested_singleton_router.register(
    "setting", UserSettingViewSet, basename="setting"
)


# API URL Build
# =============================================================================
urlpatterns = [
    *router.urls,
    *users_nested_router.urls,
    *users_nested_singleton_router.urls,
]


# Load Schema
# =============================================================================
from .schema import *
