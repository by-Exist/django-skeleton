from rest_framework.fields import empty
from .exceptions import PerformValidateOnly, BlockedSideEffect


class ValidateOnlySerializerMixin:
    def __init__(self, instance=None, data=empty, **kwargs):
        # validate only 활성화 여부에 따라
        # self에 _validate_only와 _blocked_side_effect를 기록한다.
        super().__init__(instance=instance, data=data, **kwargs)
        try:
            validate_only = self.context["view"].validate_only
            self._validate_only = validate_only
            self._blocked_side_effect = validate_only
        except (KeyError, AttributeError):
            self._validate_only = False
            self._blocked_side_effect = False

    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        if is_valid and self._validate_only:
            if raise_exception:
                msg = (
                    "rest framework의 exception handler를"
                    "drf_new_mixins.views.exception_handler로 변경할 경우"
                    "해당 exception은 자동으로 200 Response 처리됩니다."
                    "설정하지 않고 싶다면 자신의 exception_handler에"
                    "drf_new_mixins.exceptionsPerformValidateOnly의"
                    "처리 로직을 포함시키거나 뷰에서 request.validate_only의 값에 따라"
                    "직접 204 Response를 반환하는 로직을 정의해야 합니다."
                )
                raise PerformValidateOnly(msg)
            else:
                self._blocked_side_effect = True
        return is_valid

    def save(self, **kwargs):
        if self._blocked_side_effect:
            raise BlockedSideEffect("validate only 기능이 활성화되어 해당 동작을 수행할 수 없습니다.")
        return super().save(**kwargs)

    def create(self, validated_data):
        if self._blocked_side_effect:
            raise BlockedSideEffect("validate only 기능이 활성화되어 해당 동작을 수행할 수 없습니다.")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self._blocked_side_effect:
            raise BlockedSideEffect("validate only 기능이 활성화되어 해당 동작을 수행할 수 없습니다.")
        return super().update(instance, validated_data)
