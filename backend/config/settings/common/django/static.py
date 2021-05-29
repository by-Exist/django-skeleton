from pathlib import Path


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"

MEDIA_URL = "/media/"

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent

STATIC_ROOT = BASE_DIR / "static" / "static"
MEDIA_ROOT = BASE_DIR / "static" / "media"
