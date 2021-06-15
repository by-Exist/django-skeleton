from django.utils.functional import cached_property
from rest_framework.serializers import Serializer, BooleanField
from rest_framework.fields import empty
from .exceptions import PerformValidateOnly, BlockedSideEffect


class ValidateOnlySerializerMixin(Serializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        self._validate_only = self.context.pop("validate_only", False)
        self._blocked_side_effect = False

    @cached_property
    def fields(self):
        fields = super().fields
        if self._validate_only:
            validate_only_field = BooleanField(
                write_only=True, required=False, help_text="true일 경우 유효성 검사만 수행합니다."
            )
            fields["validate_only"] = validate_only_field
        return fields

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if (
            is_valid
            and self._validate_only
            and "validate_only" in self.validated_data
            and self.validated_data.pop("validate_only", False) is True
        ):
            if raise_exception:
                raise PerformValidateOnly(
                    "validate_only 필드가 포함되어 유효성 검사의 수행을 끝낸 후"
                    "is_valid에 의해 호출되는 Exception입니다."
                    "rest framework의 exception handler를"
                    "drf_validate_only.views.exception_handler로 변경할 경우"
                    "exception_handler로 인해 자동으로 200 Response 처리됩니다."
                )
            else:
                self._blocked_side_effect = True
        return is_valid

    def save(self, **kwargs):
        if self._blocked_side_effect:
            raise BlockedSideEffect("validate only가 활성화 된 요청이기에 해당 동작을 수행할 수 없습니다.")
        return super().save(**kwargs)

    def create(self, validated_data):
        if self._blocked_side_effect:
            raise BlockedSideEffect("validate only가 활성화 된 요청이기에 해당 동작을 수행할 수 없습니다.")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self._blocked_side_effect:
            raise BlockedSideEffect("validate only가 활성화 된 요청이기에 해당 동작을 수행할 수 없습니다.")
        return super().update(instance, validated_data)
