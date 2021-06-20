from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from api.urls import urlpatterns as api_urls


# Common urls
# =============================================================================
urlpatterns = [
    path(f"{settings.API_VERSION}/", include(api_urls)),
    path(
        f"{settings.API_VERSION}/schema/",
        SpectacularAPIView.as_view(api_version=settings.API_VERSION),
        name="schema",
    ),
    path(
        f"{settings.API_VERSION}/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        f"{settings.API_VERSION}/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        *urlpatterns,
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        path("__debug__/", include(debug_toolbar.urls)),
        path("api-auth/", include("rest_framework.urls")),
    ]
