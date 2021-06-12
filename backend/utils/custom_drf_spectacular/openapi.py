from django.core import validators
from drf_spectacular.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):

    method_mapping = {
        "get": "retrieve",
        "post": "create",
        "put": "replace",
        "patch": "modify",
        "delete": "destroy",
    }

    def _map_field_validators(self, field, schema):
        """
        한 필드가 여러 Regex Validator를 지닐 때 병합된 Regex pattern을 반환하도록 커스텀

        _map_field_validators를 하고서 regex를 위해 한번 더 하는 꼴이지만, 짧게 하려면...
        """

        def get_converted_pattern(pattern, validator):
            format_string = "(?={})" if not validator.inverse_match else "(?!{})"
            return format_string.format(pattern)

        def combine_regex_patterns(patterns):
            format_string = "^{}.*$"
            return format_string.format("".join(patterns))

        super()._map_field_validators(field, schema)
        regex_patterns = []

        for v in field.validators:
            if isinstance(v, validators.RegexValidator):
                pattern = v.regex.pattern.encode("ascii", "backslashreplace").decode()
                pattern = pattern.replace(r"\x", r"\u00")  # unify escaping
                pattern = pattern.replace(r"\Z", "$").replace(
                    r"\A", "^"
                )  # ECMA anchors

                if len(regex_patterns) == 0:
                    schema["pattern"] = pattern
                    regex_patterns.append(get_converted_pattern(pattern, v))
                else:
                    regex_patterns.append(get_converted_pattern(pattern, v))
                    schema["pattern"] = combine_regex_patterns(regex_patterns)
