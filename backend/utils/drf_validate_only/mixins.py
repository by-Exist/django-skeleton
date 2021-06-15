from django.utils.functional import cached_property
from rest_framework.serializers import Serializer, BooleanField
from rest_framework.fields import empty
from .exceptions import PerformValidateOnly, BlockedSideEffect


class ValidateOnlyMixin(Serializer):

    # request has body methods
    allow_validate_only_http_methods = ["POST", "PUT", "PATCH"]

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self._is_validate_only = self.get_is_validate_only()

    def get_is_validate_only(self):
        # context가 있고 view.action이 view.validate_only_actions 안에 있으며
        # request.method가 self.allow_validate_only_http_methods 안에 있어야 허용
        if not self.context:
            return False
        if "view" not in self.context or "request" not in self.context:
            return False
        view = self.context["view"]
        request = self.context["request"]
        if (
            not hasattr(view, "validate_only_actions")
            or view.action not in view.validate_only_actions
        ):
            return False
        if request.method not in self.allow_validate_only_http_methods:
            return False
        return True

    @cached_property
    def fields(self):
        fields = super().fields
        if self._is_validate_only:
            validate_only_field = BooleanField(
                write_only=True, required=False, help_text="true일 경우 유효성 검사만 수행합니다."
            )
            fields["validate_only"] = validate_only_field
        return fields

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if (
            is_valid
            and self._is_validate_only
            and "validate_only" in self.validated_data
            and self.validated_data.pop("validate_only", False) is True
        ):
            if raise_exception:
                raise PerformValidateOnly(
                    "validate_only 필드가 포함되어 유효성 검사의 수행을 끝낸 후"
                    "is_valid에 의해 호출되는 Exception입니다."
                    "rest framework의 exception handler를"
                    "drf_validate_only.views.exception_handler로 변경해주세요."
                )
            else:
                self.blocked_side_effect = True
        return is_valid

    def save(self, **kwargs):
        if hasattr(self, "blocked_side_effect"):
            raise BlockedSideEffect(
                "validate_only 필드가 포함되어 유효성 검사만을 수행해야 합니다." "save는 사용할 수 없습니다."
            )
        return super().save(**kwargs)

    def create(self, validated_data):
        if hasattr(self, "blocked_side_effect"):
            raise BlockedSideEffect(
                "validate_only 필드가 포함되어 유효성 검사만을 수행해야 합니다." "create는 사용할 수 없습니다."
            )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if hasattr(self, "blocked_side_effect"):
            raise BlockedSideEffect(
                "validate_only 필드가 포함되어 유효성 검사만을 수행해야 합니다." "update는 사용할 수 없습니다."
            )
        return super().update(instance, validated_data)
