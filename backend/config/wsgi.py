import os

from django.core.wsgi import get_wsgi_application

assert "DJANGO_SETTINGS_MODULE" in os.environ, "DJANGO_SETTINGS_MODULE 환경변수가 필요합니다."

application = get_wsgi_application()
