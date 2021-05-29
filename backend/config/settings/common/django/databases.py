import environ


env = environ.Env()


# Database
DATABASES = {"default": env.db("DJANGO_DEFAULT_DATABASE_URL")}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
