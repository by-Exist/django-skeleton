from rest_framework.routers import (
    escape_curly_brackets,
    Route,
    DynamicRoute,
    SimpleRouter,
    DefaultRouter,
)
from rest_framework_nested.routers import NestedMixin


# routes
# =============================================================================
custom_method_default_routes = [
    # List
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "list", "post": "create"},
        name="{basename}-list",
        detail=False,
        initkwargs={"suffix": "List"},
    ),
    # Action(detail=False)
    DynamicRoute(
        url=r"^{prefix}{slash}{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=False,
        initkwargs={},
    ),
    # Detail
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
    # Action(detail=True)
    DynamicRoute(
        url=r"^{prefix}/{lookup}{slash}{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]

sub_resource_singleton_routes = [
    # Detail
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "replace", "patch": "modify"},
        name="{basename}-detail",
        detail=True,
        initkwargs={"suffix": "Instance"},
    ),
    # Action(detail=True)
    DynamicRoute(
        url=r"^{prefix}{slash}{url_path}{trailing_slash}$",
        name="{basename}-{url_name}",
        detail=True,
        initkwargs={},
    ),
]


# Mixins
# =============================================================================
class CustomMethodMixin:
    """
    Router가 CustomMethod 동작을 지원하도록 수정하는 용도의 Mixin

    custom_drf.decorators의 action에 종속적이다.

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    """

    def _get_dynamic_route(self, route, action):
        initkwargs = route.initkwargs.copy()
        initkwargs.update(action.kwargs)
        url_path = escape_curly_brackets(action.url_path)
        # here
        slash = ":" if action.custom_method else "/"
        return Route(
            # here
            url=route.url.replace("{url_path}", url_path).replace("{slash}", slash),
            mapping=action.mapping,
            name=route.name.replace("{url_name}", action.url_name),
            detail=route.detail,
            initkwargs=initkwargs,
        )

    def get_lookup_regex(self, viewset, lookup_prefix=""):
        base_regex = "(?P<{lookup_prefix}{lookup_url_kwarg}>{lookup_value})"
        lookup_field = getattr(viewset, "lookup_field", "pk")
        lookup_url_kwarg = getattr(viewset, "lookup_url_kwarg", None) or lookup_field
        # here
        lookup_value = getattr(viewset, "lookup_value_regex", "[^/.:]+")
        result = base_regex.format(
            lookup_prefix=lookup_prefix,
            lookup_url_kwarg=lookup_url_kwarg,
            lookup_value=lookup_value,
        )
        return result


# Routers
# =============================================================================
class CustomMethodSimpleRouter(CustomMethodMixin, SimpleRouter):
    """
    CustomMethod 동작을 지원하는 SimpleRouter

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다
    """

    routes = custom_method_default_routes


class CustomMethodDefaultRouter(CustomMethodMixin, DefaultRouter):
    """
    CustomMethod 동작을 지원하는 DefaultRouter

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다
    """

    routes = custom_method_default_routes


class NestedCustomMethodSimpleRouter(NestedMixin, CustomMethodSimpleRouter):
    """
    CustomMethod 동작을 지원하는 NestedSimpleRouter

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다
    """

    pass


class NestedCustomMethodDefaultRouter(NestedMixin, CustomMethodDefaultRouter):
    """
    CustomMethod 동작을 지원하는 NestedDefaultRouter

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다
    """

    pass


class NestedSingletonResourceCustomMethodSimpleRouter(NestedCustomMethodSimpleRouter):
    """
    CustomMethod 동작을 지원하며 리소스가 싱글 톤일 때 활용되는 NestedSimpleRouter

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다
    """

    routes = sub_resource_singleton_routes


class NestedSingletonResourceCustomMethodDefaultRouter(NestedCustomMethodDefaultRouter):
    """
    CustomMethod 동작을 지원하며 리소스가 싱글 톤일 때 활용되는 NestedDefaultRouter

    lookup_value_regex가 정의되지 않았을 경우 사용되는 기본값이 [^/.]에서 [^/.:]로 변경
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다
    """

    routes = sub_resource_singleton_routes
