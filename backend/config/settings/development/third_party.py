from .django import *
from debug_toolbar.settings import PANELS_DEFAULTS


# Django Debug Toolbar
# =============================================================================
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
DEBUG_TOOLBAR_CONFIG = {}
DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"] = lambda request: True


# Django Extensions
# =============================================================================
INSTALLED_APPS += ["django_extensions"]


# DRF Spectacular
# =============================================================================
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS["TITLE"] = "Backend Development API"
SPECTACULAR_SETTINGS["DESCRIPTION"] = "Backend development api description..."
SPECTACULAR_SETTINGS["VERSION"] = "0.0.1"
# https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
SPECTACULAR_SETTINGS["SWAGGER_UI_SETTINGS"]["displayRequestDuration"] = True


# Django Cachalot
# =============================================================================
# https://django-cachalot.readthedocs.io/en/latest/quickstart.html#settings
INSTALLED_APPS += ["cachalot"]
CACHES["cachalot"] = env.cache("DJANGO_CACHALOT_CACHE_URL")
CACHALOT_CACHE = "cachalot"
CACHALOT_UNCACHABLE_TABLES = ["django_migrations"]
PANELS_DEFAULTS += ["cachalot.panels.CachalotPanel"]
