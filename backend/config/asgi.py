import os

from django.core.asgi import get_asgi_application

assert "DJANGO_SETTINGS_MODULE" in os.environ, "DJANGO_SETTINGS_MODULE 환경변수가 필요합니다."

application = get_asgi_application()
