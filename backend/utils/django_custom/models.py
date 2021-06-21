from django.conf import settings
from django.urls import reverse, resolve


class ResourceNameModelMixin:
    @property
    def resource_name(self):
        url = self.get_absolute_url()
        resource_name = url.lstrip(f"/{settings.API_VERSION}")
        return resource_name

    @property
    def full_resource_name(self):
        full_resource_name = settings.API_SERVICE_NAME + "/" + self.resource_name
        return full_resource_name

    def __str__(self) -> str:
        return self.full_resource_name
