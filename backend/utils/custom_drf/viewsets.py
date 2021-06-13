from rest_framework.viewsets import GenericViewSet as OriginGenericViewSet
from .mixins import AddValidateOnlyFieldMixin, CheckPageableMixin


class GenericViewSet(
    AddValidateOnlyFieldMixin, CheckPageableMixin, OriginGenericViewSet
):
    pass
