from .django import *
from rest_framework.settings import DEFAULTS
from drf_spectacular.settings import SPECTACULAR_DEFAULTS


# Django REST Framework
# =============================================================================
# https://www.django-rest-framework.org/api-guide/settings/
INSTALLED_APPS += ["rest_framework"]
REST_FRAMEWORK = DEFAULTS


# DRF Spectacular
# =============================================================================
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK[
    "DEFAULT_SCHEMA_CLASS"
] = "utils.custom_drf_spectacular.openapi.CustomAutoSchema"
SPECTACULAR_SETTINGS = SPECTACULAR_DEFAULTS
SPECTACULAR_SETTINGS["SCHEMA_PATH_PREFIX"] = "/api/v[0-9]+/"
SPECTACULAR_SETTINGS["COMPONENT_SPLIT_REQUEST"] = True
SPECTACULAR_SETTINGS["SERVE_INCLUDE_SCHEMA"] = False


# Django Cachalot
# =============================================================================
# https://django-cachalot.readthedocs.io/en/latest/quickstart.html#settings
INSTALLED_APPS += ["cachalot"]
CACHES["cachalot"] = env.cache("DJANGO_CACHALOT_CACHE_URL")
CACHALOT_CACHE = "cachalot"
CACHALOT_UNCACHABLE_TABLES = ["django_migrations"]
