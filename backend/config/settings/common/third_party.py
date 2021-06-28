from .django import *


# Django REST Framework
# =============================================================================
# https://www.django-rest-framework.org/api-guide/settings/
INSTALLED_APPS += ["rest_framework"]
REST_FRAMEWORK = {}
REST_FRAMEWORK["DEFAULT_FILTER_BACKENDS"] = []


# Django Filter
# =============================================================================
# https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html
INSTALLED_APPS += ["django_filters"]
REST_FRAMEWORK["DEFAULT_FILTER_BACKENDS"] += [
    "django_filters.rest_framework.DjangoFilterBackend"
]


# DRF Spectacular
# =============================================================================
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
INSTALLED_APPS += ["drf_spectacular"]
REST_FRAMEWORK["DEFAULT_SCHEMA_CLASS"] = "utils.drf_custom.openapi.CustomAutoSchema"
SPECTACULAR_SETTINGS = {}
SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"] = {}
SPECTACULAR_SETTINGS["SCHEMA_PATH_PREFIX"] = "/v[0-9]+/"
SPECTACULAR_SETTINGS["COMPONENT_SPLIT_REQUEST"] = True
SPECTACULAR_SETTINGS["SERVE_INCLUDE_SCHEMA"] = False


# Django Cachalot
# =============================================================================
# https://django-cachalot.readthedocs.io/en/latest/quickstart.html#settings
# INSTALLED_APPS += ["cachalot"]
# CACHES["cachalot"] = env.cache("DJANGO_CACHALOT_CACHE_URL")
# CACHALOT_CACHE = "cachalot"
# CACHALOT_UNCACHABLE_TABLES = ["django_migrations"]
