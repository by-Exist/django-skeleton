import uritemplate
from django.db import models
from django.core import exceptions as django_exceptions
from drf_spectacular.extensions import OpenApiFilterExtension
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.settings import spectacular_settings
from drf_spectacular.plumbing import (
    build_basic_type,
    build_parameter_type,
    resolve_regex_path_parameter,
    get_view_model,
    warn,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


def get_pk_description(model, model_field):
    # id 필드의 description을 생성하는 함수
    # 한글로 변환하기 위해서 해당 함수를 재작성하였다.
    if isinstance(model_field, models.AutoField):
        value_type = "unique한 정수"
    elif isinstance(model_field, models.UUIDField):
        value_type = "UUID 문자열"
    else:
        value_type = "unique한 값"

    return "{name} 리소스를 식별하는 {value_type}입니다.".format(
        value_type=value_type, name=model._meta.verbose_name,
    )


class CustomAutoSchema(AutoSchema):
    def _get_filter_parameters(self):
        # filter_backends를 올바르게 불러오지 못하는 문제가 있어 수정
        # view.filter_backends가 프로퍼티이며 filter_backends 또는 None을 반환해야 한다.
        filter_backends = getattr(self.view, "filter_backends", None)
        if not filter_backends:
            return []
        parameters = []
        for filter_backend in filter_backends:
            filter_extension = OpenApiFilterExtension.get_match(filter_backend())
            if filter_extension:
                parameters += filter_extension.get_schema_operation_parameters(self)
            else:
                parameters += filter_backend().get_schema_operation_parameters(
                    self.view
                )
        return parameters

    def _get_parameters(self):
        # _get_validate_only_parameters 과정을 추가하였다.
        def dict_helper(parameters):
            return {(p["name"], p["in"]): p for p in parameters}

        override_parameters = self._process_override_parameters()
        path_variables = [
            v
            for v in uritemplate.variables(self.path)
            if (v, "path") not in override_parameters
        ]
        parameters = {
            **dict_helper(self._resolve_path_parameters(path_variables)),
            **dict_helper(self._get_filter_parameters()),
            **dict_helper(self._get_pagination_parameters()),
            **dict_helper(self._get_format_parameters()),
            **dict_helper(self._get_validate_only_parameters()),
        }
        for key, parameter in override_parameters.items():
            if parameter is None:
                if key in parameters:
                    del parameters[key]
            else:
                parameters[key] = parameter

        if callable(spectacular_settings.SORT_OPERATION_PARAMETERS):
            return sorted(
                parameters.values(), key=spectacular_settings.SORT_OPERATION_PARAMETERS
            )
        elif spectacular_settings.SORT_OPERATION_PARAMETERS:
            return sorted(parameters.values(), key=lambda p: p["name"])
        else:
            return list(parameters.values())

    def _get_validate_only_parameters(self):
        validate_only_actions = getattr(self.view, "validate_only_actions", None)
        if validate_only_actions is None:
            return []
        if self.view.action not in validate_only_actions:
            return []
        return [
            {
                "name": "validate_only",
                "required": False,
                "in": "query",
                "description": "true일 경우 입력 필드의 유효성 검사만 수행합니다.",
                "schema": {"type": "boolean",},
            },
        ]

    def _resolve_path_parameters(self, variables):
        parameters = []
        for variable in variables:
            schema = build_basic_type(OpenApiTypes.STR)
            description = ""

            resolved_parameter = resolve_regex_path_parameter(
                self.path_regex, variable, self.map_renderers("format"),
            )

            if resolved_parameter:
                schema = resolved_parameter["schema"]
            elif get_view_model(self.view) is None:
                warn(
                    f'could not derive type of path parameter "{variable}" because because it '
                    f"is untyped and obtaining queryset from the viewset failed. "
                    f"Consider adding a type to the path (e.g. <int:{variable}>) or annotating "
                    f'the parameter type with @extend_schema. Defaulting to "string".'
                )
            else:
                try:
                    model = get_view_model(self.view)
                    model_field = model._meta.get_field(variable)
                    schema = self._map_model_field(model_field, direction=None)
                    if "description" not in schema and model_field.primary_key:
                        description = get_pk_description(model, model_field)
                except django_exceptions.FieldDoesNotExist:
                    warn(
                        f'could not derive type of path parameter "{variable}" because '
                        f'model "{model}" did contain no such field. Consider annotating '
                        f'parameter with @extend_schema. Defaulting to "string".'
                    )

            parameters.append(
                build_parameter_type(
                    name=variable,
                    location=OpenApiParameter.PATH,
                    description=description,
                    schema=schema,
                )
            )

        return parameters
