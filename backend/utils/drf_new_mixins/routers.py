from rest_framework import routers as rest_routers
from rest_framework_nested.routers import NestedMixin


# Mixins
# =============================================================================
class CustomMethodRouterMixin:
    def get_lookup_regex(self, viewset, lookup_prefix=""):
        # custom method가 적용된 경우 lookup_value_regex를 변경
        # "[^/.]" => "[^/.:]"
        base_regex = "(?P<{lookup_prefix}{lookup_url_kwarg}>{lookup_value})"
        lookup_field = getattr(viewset, "lookup_field", "pk")
        lookup_url_kwarg = getattr(viewset, "lookup_url_kwarg", None) or lookup_field
        lookup_value = getattr(viewset, "lookup_value_regex", "[^/.:]+")
        result = base_regex.format(
            lookup_prefix=lookup_prefix,
            lookup_url_kwarg=lookup_url_kwarg,
            lookup_value=lookup_value,
        )
        return result


# Routes
# =============================================================================
routes = [
    rest_routers.Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "list", "post": "create"},
        name="{basename}-list",
        detail=False,
        initkwargs={"suffix": "List"},
    ),
    rest_routers.DynamicRoute(
        url=r"^{prefix}/{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=False,
        initkwargs={},
    ),
    rest_routers.Route(
        url=r"^{prefix}/{lookup}{trailing_slash}$",
        mapping={
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        },
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    rest_routers.DynamicRoute(
        url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]

nested_singleton_routes = [
    rest_routers.Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "update", "patch": "partial_update"},
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    rest_routers.DynamicRoute(
        url=r"^{prefix}/{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]

custom_routes = [
    rest_routers.Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "list", "post": "create"},
        name="{basename}-list",
        detail=False,
        initkwargs={"suffix": "List"},
    ),
    rest_routers.DynamicRoute(
        url=r"^{prefix}:{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=False,
        initkwargs={},
    ),
    rest_routers.Route(
        url=r"^{prefix}/{lookup}{trailing_slash}$",
        mapping={
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        },
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    rest_routers.DynamicRoute(
        url=r"^{prefix}/{lookup}:{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]

custom_nested_singleton_routes = [
    rest_routers.Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "update", "patch": "partial_update"},
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    rest_routers.DynamicRoute(
        url=r"^{prefix}:{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]


# Routers
# =============================================================================
class SimpleRouter(rest_routers.SimpleRouter):
    routes = routes


class DefaultRouter(rest_routers.DefaultRouter):
    routes = routes


class NestedSimpleRouter(NestedMixin, rest_routers.SimpleRouter):
    routes = routes


class NestedDefaultRouter(NestedMixin, rest_routers.DefaultRouter):
    routes = routes


class NestedSingletonSimpleRouter(NestedMixin, rest_routers.SimpleRouter):
    routes = nested_singleton_routes


class NestedSingletonDefaultRouter(NestedMixin, rest_routers.DefaultRouter):
    routes = nested_singleton_routes


class CustomSimpleRouter(CustomMethodRouterMixin, rest_routers.SimpleRouter):
    routes = custom_routes


class CustomDefaultRouter(CustomMethodRouterMixin, rest_routers.DefaultRouter):
    routes = custom_routes


class CustomNestedSimpleRouter(
    CustomMethodRouterMixin, NestedMixin, rest_routers.SimpleRouter
):
    routes = custom_routes


class CustomNestedDefaultRouter(
    CustomMethodRouterMixin, NestedMixin, rest_routers.DefaultRouter
):
    routes = custom_routes


class CustomNestedSingletonSimpleRouter(
    CustomMethodRouterMixin, NestedMixin, rest_routers.SimpleRouter,
):
    routes = custom_nested_singleton_routes


class CustomNestedSingletonDefaultRouter(
    CustomMethodRouterMixin, NestedMixin, rest_routers.DefaultRouter,
):
    routes = custom_nested_singleton_routes
