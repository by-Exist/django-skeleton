from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from api.urls import API_VERSION, urlpatterns as api_urls


# Common urls
# =============================================================================
urlpatterns = [
    path(f"<version:version>/", include(api_urls)),
    path(
        "<version:version>/schema/",
        SpectacularAPIView.as_view(api_version=API_VERSION),
        name="schema",
    ),
    path(
        "<version:version>/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "<version:version>/schema/redoc/",
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
