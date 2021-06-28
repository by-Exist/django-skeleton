import re
from django.template import loader
from django.utils.encoding import force_str
from rest_framework import (
    filters as rest_filters,
    exceptions as rest_exceptions,
)
from rest_framework.compat import coreapi, coreschema


class OrderingFilterBackend(rest_filters.BaseFilterBackend):
    """
    Required

      - "ordering_fields" : ['id', 'created_time', ...]

    Can Overwrite

      - "ordering_param" : "ordering"
    """

    ordering_param = "ordering"
    ordering_title = "정렬"
    ordering_description = "결과 정렬에 사용되는 필드입니다."
    template = "rest_framework/filters/ordering.html"

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            return queryset.order_by(*ordering)
        return queryset

    def get_ordering(self, request, queryset, view):
        ordering_param = getattr(view, "ordering_param", self.ordering_param)
        params = request.query_params.get(ordering_param)
        if params:
            fields = [
                "-" + param.strip()[:-5] if param.endswith(" desc") else param.strip()
                for param in params.split(",")
            ]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering
        return None

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = [
            item[0]
            for item in self.get_valid_fields(queryset, view, {"request": request})
        ]

        def term_valid(term):
            if term.endswith(" desc"):
                term = term[:-5]
            return term in valid_fields

        return [term for term in fields if term_valid(term)]

    def get_valid_fields(self, queryset, view, context={}):
        valid_fields = getattr(view, "ordering_fields", None)
        if valid_fields is None:
            return []
        valid_fields = [
            (item, item) if isinstance(item, str) else item for item in valid_fields
        ]
        return valid_fields

    def to_html(self, request, queryset, view):
        if not getattr(view, "ordering_fields", None):
            return ""
        template = loader.get_template(self.template)
        context = self.get_template_context(request, queryset, view)
        return template.render(context)

    def get_template_context(self, request, queryset, view):
        current = self.get_ordering(request, queryset, view)
        current = None if not current else current[0]
        options = []
        context = {
            "request": request,
            "current": current,
            "param": getattr(view, "ordering_param", self.ordering_param),
        }
        for key, label in self.get_valid_fields(queryset, view, context):
            options.append((key, "%s - %s" % (label, "오름차순")))
            options.append((key + " desc", "%s - %s" % (label, "내림차순")))
        context["options"] = options
        return context

    def get_schema_fields(self, view):
        if not getattr(view, "ordering_fields", None):
            return []
        assert (
            coreapi is not None
        ), "coreapi must be installed to use `get_schema_fields()`"
        assert (
            coreschema is not None
        ), "coreschema must be installed to use `get_schema_fields()`"
        useable_values = ", ".join(
            [
                *[f'"{field}"' for field in view.ordering_fields],
                *[f'"{field} desc"' for field in view.ordering_fields],
            ]
        )
        ordering_description = "{}\n\n사용 가능한 값들 = [{}]".format(
            self.ordering_description, useable_values
        )
        return [
            coreapi.Field(
                name=getattr(view, "ordering_param", self.ordering_param),
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(self.ordering_title),
                    description=force_str(ordering_description),
                ),
            )
        ]

    def get_schema_operation_parameters(self, view):
        if not getattr(view, "ordering_fields", None):
            return []

        useable_values = ", ".join(
            [
                *[f'"{field}"' for field in view.ordering_fields],
                *[f'"{field} desc"' for field in view.ordering_fields],
            ]
        )
        ordering_description = "{}\n\n사용 가능한 값들 = [{}]".format(
            self.ordering_description, useable_values
        )
        return [
            {
                "name": getattr(view, "ordering_param", self.ordering_param),
                "required": False,
                "in": "query",
                "description": force_str(ordering_description),
                "schema": {"type": "string",},
            },
        ]


class BatchGetFilterBackend(rest_filters.BaseFilterBackend):
    """
    Required

      - "batch_get_value_regex" : "^[0-9]+$"

    Can Overwrite

      - "batch_get_lookup_field" : f"{field}__in"

      - "batch_get_param" : ?valueList=1,2,3

      - "batch_get_limit" : over, raise ValidationError
    """

    batch_get_param = "valueList"
    batch_get_limit = 200
    batch_get_description = (
        "콤마(,)로 구분된 식별자들을 활용하여 리소스들을 일괄적으로 가져옵니다.\n\n"
        "가져올 수 없는 경우(올바르지 않은 식별자, 존재하지 않는 리소스)는 무시됩니다."
    )

    def filter_queryset(self, request, queryset, view):

        lookup_field = getattr(view, "batch_get_lookup_field", view.lookup_field)  # pk
        lookup_value_regex = view.batch_get_value_regex  # required
        query_expr = f"{lookup_field}__in"  # "pk__in"

        batch_get_param = getattr(view, "batch_get_param", self.batch_get_param)
        values = self.get_lookup_values(request, batch_get_param, lookup_value_regex)
        if not values:
            raise rest_exceptions.ValidationError(
                detail={f"{batch_get_param}": f"required query string."},
            )
        batch_get_limit = getattr(view, "batch_get_limit", self.batch_get_limit)
        if len(values) > batch_get_limit:
            raise rest_exceptions.ValidationError(
                detail={
                    f"{batch_get_param}": f"Over batch get limit count. (input={len(values)}, allow={self.batch_get_limit})"
                },
            )
        queryset = queryset.filter(**{query_expr: values})
        return queryset

    def get_lookup_values(self, request, batch_get_param, lookup_value_regex):
        csv_value = request.query_params.get(batch_get_param)
        if csv_value:
            lookup_values = [
                value.strip()
                for value in csv_value.split(",")
                if re.match(lookup_value_regex, value.strip())
            ]
            return lookup_values
        return None

    def get_schema_fields(self, view):
        return super().get_schema_fields(view)

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": getattr(view, "batch_get_param", self.batch_get_param),
                "required": True,
                "in": "query",
                "description": force_str(self.batch_get_description),
                "schema": {"type": "string",},
            },
        ]


class PathVariableFilterBackend(rest_filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        path_variable_config = getattr(view, "path_variable_config", None)
        if not path_variable_config:
            return queryset
        for lookup_url_kwarg, options in path_variable_config.items():
            field = options["field"]
            lookup_value = view.kwargs[lookup_url_kwarg]
            if lookup_value == "-":
                continue
            queryset = queryset.filter(**{field: lookup_value})
        return queryset

    def get_schema_fields(self, view):
        return super().get_schema_fields(view)

    def get_schema_operation_parameters(self, view):
        wildcard_description = "와일드카드(-) 문법이 허용됩니다."
        result = []
        for lookup_url_kwarg, options in view.path_variable_config.items():
            allow_wildcard_actions = options["allow_wildcard_actions"]
            path_param = {
                "name": lookup_url_kwarg,
                "required": True,
                "in": "path",
                "description": ""
                if view.action not in allow_wildcard_actions
                else wildcard_description,
                "schema": {"type": "string",},
            }
            result.append(path_param)
        return result
