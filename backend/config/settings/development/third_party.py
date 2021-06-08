from .django import *


# Django Debug Toolbar
# =============================================================================
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}


# Django REST Framework
# =============================================================================
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK[
    "DEFAULT_VERSIONING_CLASS"
] = "rest_framework.versioning.URLPathVersioning"


# DRF Spectacular
# =============================================================================
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "drf_spectacular.openapi.AutoSchema"
SPECTACULAR_SETTINGS["TITLE"] = "Backend Development API"
SPECTACULAR_SETTINGS["DESCRIPTION"] = "Backend development api description..."
SPECTACULAR_SETTINGS["VERSION"] = "0.0.1"
