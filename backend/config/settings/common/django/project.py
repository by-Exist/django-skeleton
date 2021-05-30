from pathlib import Path
import environ


env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

DEBUG = env.bool("DJANGO_DEBUG")

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

ROOT_URLCONF = "api.urls"

WSGI_APPLICATION = "config.wsgi.application"
