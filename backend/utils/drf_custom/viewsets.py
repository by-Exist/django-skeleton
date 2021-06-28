from rest_framework import viewsets as rest_viewsets
from rest_framework.exceptions import NotFound
from .serializers import ValidateOnlySerializerMixin


class ValidateOnlyGenericViewSetMixin:

    validate_only_param = "validate_only"
    validate_only_actions = []
    validate_only_allow_param_values = frozenset(("true",))

    _validate_only_allow_request_methods = frozenset(("POST", "PUT", "PATCH"))
    _validate_only_serializer_registry = {}

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.validate_only:
            return self.get_validate_only_serializer_class(serializer_class)
        return serializer_class

    @property
    def validate_only(self):
        if (
            self.action in self.validate_only_actions
            and self.request.method in self._validate_only_allow_request_methods
            and self.request.query_params.get(self.validate_only_param, "")
            in self.validate_only_allow_param_values
        ):
            return True
        return False

    def get_validate_only_serializer_class(self, serializer_class):
        validate_only_serializer_class_name = "ValidateOnly" + serializer_class.__name__
        if (
            validate_only_serializer_class_name
            in self._validate_only_serializer_registry
        ):
            return self._validate_only_serializer_registry[
                validate_only_serializer_class_name
            ]
        validate_only_serializer_class = type(
            validate_only_serializer_class_name,
            (ValidateOnlySerializerMixin, serializer_class),
            {},
        )
        self._validate_only_serializer_registry[
            validate_only_serializer_class_name
        ] = validate_only_serializer_class
        return validate_only_serializer_class


class CheckPathVariableViewSetMixin(rest_viewsets.GenericViewSet):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_path_variable()

    def check_path_variable(self):
        path_variable_config = getattr(self, "path_variable_config", None)
        if path_variable_config is None:
            return
        for lookup_url_kwarg, options in path_variable_config.items():
            lookup_value = self.kwargs[lookup_url_kwarg]
            allow_wildcard_actions = options["allow_wildcard_actions"]
            if lookup_value == "-" and self.action not in allow_wildcard_actions:
                raise NotFound()


class GenericViewSet(
    ValidateOnlyGenericViewSetMixin,
    CheckPathVariableViewSetMixin,
    rest_viewsets.GenericViewSet,
):
    pass
