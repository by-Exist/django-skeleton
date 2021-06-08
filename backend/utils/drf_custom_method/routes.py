from rest_framework.routers import Route, DynamicRoute


# Custom Method Routes
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
            "put": "update",
            "patch": "partial_update",
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


# Nested Singleton Resource Custom Method Routers
# =============================================================================
sub_resource_singleton_routes = [
    # Detail
    Route(
        url=r"^{prefix}{trailing_slash}$",
        mapping={"get": "retrieve", "put": "update", "patch": "partial_update",},
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
