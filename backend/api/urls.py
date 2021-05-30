from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, register_converter
from drf_custom_method.routers import CustomMethodSimpleRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
import debug_toolbar
from apps.exampleapp.views import ExampleViewSet
from .converters import VersionConverter


# API Version    TODO: Move settings?
# =============================================================================
API_VERSION = "v1"


# Set Converters
# =============================================================================
register_converter(VersionConverter, "version")


# Router
# =============================================================================
api_router = CustomMethodSimpleRouter()
api_router.trailing_slash = "/?"


# API URL Build
# =============================================================================
api_router.register("examples", ExampleViewSet, basename="example")

api_urls = [
    *api_router.urls,
]


# Result URLs
# =============================================================================
urlpatterns = [
    # Admin urls
    path("admin/", admin.site.urls),
    # DRF Browserable urls
    path("api-auth/", include("rest_framework.urls")),
    # API urls
    path(f"api/<version:version>/", include(api_urls)),
    # Schema urls
    path(
        "api/<version:version>/schema/",
        SpectacularAPIView.as_view(api_version=API_VERSION),
        name="schema",
    ),
    path(
        "api/<version:version>/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
    path(
        "api/<version:version>/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if settings.DEBUG:
    urlpatterns = [
        # Common urls
        *urlpatterns,
        # Serving static file urls
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        # Debug toolbar urls
        path("__debug__/", include(debug_toolbar.urls)),
    ]


# Load Schema
# =============================================================================
from .schema import *
