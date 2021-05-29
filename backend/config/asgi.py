"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

assert "DJANGO_SETTINGS_MODULE" in os.environ, "DJANGO_SETTINGS_MODULE 환경변수가 필요합니다."

application = get_asgi_application()
