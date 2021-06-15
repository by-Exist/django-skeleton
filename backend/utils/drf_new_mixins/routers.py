from rest_framework import routers
from rest_framework.routers import Route, DynamicRoute
from rest_framework_nested.routers import NestedMixin


# Routes
# =============================================================================
new_mixin_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "list", "post": "create"},
        name="{basename}-list",
        detail=False,
        initkwargs={"suffix": "List"},
    ),
    DynamicRoute(
        url=r"^{prefix}/{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=False,
        initkwargs={},
    ),
    Route(
        url=r"^{prefix}/{lookup}{trailing_slash}$",
        mapping={
            "get": "retrieve",
            "put": "replace",
            "patch": "modify",
            "delete": "destroy",
        },
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    DynamicRoute(
        url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]

new_mixin_singleton_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "replace", "patch": "modify"},
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    DynamicRoute(
        url=r"^{prefix}/{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]


# Mixins
# =============================================================================
class NotAllowCreateDestroyMixin:
    # TODO: 내일 할 작업.
    pass


# Routers
# =============================================================================
class SimpleRouter(routers.SimpleRouter):
    routes = new_mixin_routes


class DefaultRouter(routers.DefaultRouter):
    routes = new_mixin_routes


class NestedSimpleRouter(NestedMixin, routers.SimpleRouter):
    routes = new_mixin_routes


class NestedDefaultRouter(NestedMixin, routers.DefaultRouter):
    routes = new_mixin_routes


class NestedSingletonSimpleRouter(
    NestedMixin, NotAllowCreateDestroyMixin, routers.SimpleRouter
):
    routes = new_mixin_singleton_routes


class NestedSingletonDefaultRouter(
    NestedMixin, NotAllowCreateDestroyMixin, routers.DefaultRouter
):
    routes = new_mixin_singleton_routes
