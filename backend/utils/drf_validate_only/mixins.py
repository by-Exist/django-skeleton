from rest_framework.viewsets import GenericViewSet
from .serializers import ValidateOnlySerializerMixin


class ValidateOnlyAPIViewMixin(GenericViewSet):
    validate_only_actions = []
    allow_validate_only_http_methods = ["POST", "PUT", "PATCH"]

    @property
    def _enable_validate_only(self):
        if self.action not in self.validate_only_actions:
            return False
        if self.request.method not in self.allow_validate_only_http_methods:
            msg = "validate only 기능은 body가 존재하는 http request method에서만 활용할 수 있습니다."
            raise AssertionError(msg)
        return True

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self._enable_validate_only:
            context["validate_only"] = True
        return context

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if not issubclass(serializer_class, ValidateOnlySerializerMixin):
            msg = (
                "validate only 기능을 활용하기 위해서는 {}가"
                "ValidateOnlySerializerMixin을 상속해야 합니다."
            ).format(serializer_class.__name__)
            raise AssertionError(msg)
        return serializer_class
