from rest_framework.routers import Route, escape_curly_brackets
from rest_framework_nested.routers import NestedMixin


class CustomMethodMixin:
    """
    Router의 CustomMethod 동작을 지원하기 작성된 Mixin

    [Google API Guide - CustomMethod](https://cloud.google.com/apis/design/custom_methods?hl=ko)

    action.custom_method 속성을 읽어야 하기 때문에 drf_custom_method.decorators의 custom_action에 종속적이다.

    lookup_value_regex가 [^/.]에서 [^/.:]로 변경된다.
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다.
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
