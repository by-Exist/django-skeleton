from .django import *


# Django Storage
# =============================================================================
STATICFILES_STORAGE = "config.storages.StaticStorage"
DEFAULT_FILE_STORAGE = "config.storages.MediaStorage"
AWS_S3_REGION_NAME = "ewr1"
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.vultrobjects.com/"
AWS_ACCESS_KEY_ID = env.str("DJANGO_STORAGE_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("DJANGO_STORAGE_SECRET_ACCESS_KEY")


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
