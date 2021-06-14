class CustomMethodRouterMixin:
    def _get_dynamic_route(self, route, action):
        """action.custom_method가 True라면 라우터의 /를 :로 변경"""
        route = super()._get_dynamic_route(route, action)
        if hasattr(action, "custom_method") and action.custom_method:
            new_route = route._replace(
                url=route.url.replace(f"/{action.url_path}", f":{action.url_path}")
            )
            return new_route
        return route

    def get_lookup_regex(self, viewset, lookup_prefix=""):
        """lookup_value를 [^/.]에서 [^/.:]로 변경"""
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
