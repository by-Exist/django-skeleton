# DRF SPECTACULAR CONFIGURATION
# =============================================================================
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
description = "API description..."

SPECTACULAR_SETTINGS = {
    # Metadata
    "TITLE": "API Title",
    "DESCRIPTION": description,
    "VERSION": "0.0.1",
    # Swagger settings
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
    # Spectacular settings
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "SORT_OPERATION_PARAMETERS": False,
    "SERVE_AUTHENTICATION": None,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
}
