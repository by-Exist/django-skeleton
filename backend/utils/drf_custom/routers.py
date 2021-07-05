from rest_framework.routers import Route, DynamicRoute


# Mixins
# =============================================================================
from rest_framework_nested.routers import NestedMixin


class CustomMethodMixin:
    def get_lookup_regex(self, viewset, lookup_prefix=""):
        # lookup_value_regex를 [^/.]에서 [^/.:]로 변경
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
nested_singleton_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "update", "patch": "partial_update"},
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

custom_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "list", "post": "create"},
        name="{basename}-list",
        detail=False,
        initkwargs={"suffix": "List"},
    ),
    DynamicRoute(
        url=r"^{prefix}:{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=False,
        initkwargs={},
    ),
    Route(
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
    DynamicRoute(
        url=r"^{prefix}/{lookup}:{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]

custom_nested_singleton_routes = [
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "update", "patch": "partial_update"},
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    DynamicRoute(
        url=r"^{prefix}:{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]


# Routers
# =============================================================================
from rest_framework.routers import SimpleRouter


from rest_framework.routers import DefaultRouter


class NestedSimpleRouter(NestedMixin, SimpleRouter):
    pass


class NestedDefaultRouter(NestedMixin, DefaultRouter):
    pass


class NestedSingletonSimpleRouter(NestedMixin, SimpleRouter):
    routes = nested_singleton_routes


class NestedSingletonDefaultRouter(NestedMixin, DefaultRouter):
    routes = nested_singleton_routes


class CustomSimpleRouter(CustomMethodMixin, SimpleRouter):
    routes = custom_routes


class CustomDefaultRouter(CustomMethodMixin, DefaultRouter):
    routes = custom_routes


class CustomNestedSimpleRouter(CustomMethodMixin, NestedMixin, SimpleRouter):
    routes = custom_routes


class CustomNestedDefaultRouter(CustomMethodMixin, NestedMixin, DefaultRouter):
    routes = custom_routes


class CustomNestedSingletonSimpleRouter(
    CustomMethodMixin,
    NestedMixin,
    SimpleRouter,
):
    routes = custom_nested_singleton_routes


class CustomNestedSingletonDefaultRouter(
    CustomMethodMixin,
    NestedMixin,
    DefaultRouter,
):
    routes = custom_nested_singleton_routes
