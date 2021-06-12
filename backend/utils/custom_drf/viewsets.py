from rest_framework.serializers import BooleanField
from rest_framework.viewsets import GenericViewSet


class ValidateOnlyMixin:
    """
    만약 viewset에 validate_only_actions 클래스 속성이 정의되어 있다면

    해당 action의 get_serializer가 수행될 때 validate_only 필드를 동적으로 추가하는 믹스인.
    """

    validate_only_actions = []
    allow_validate_only_actions = ["create", "replace", "modify"]

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        # here
        if not self.validate_only_actions:
            return serializer

        assert (
            self.action in self.allow_validate_only_actions
        ), "validate_only 기능은 {} 액션에서만 사용할 수 있습니다.".format(
            ", ".join(self.allow_validate_only_actions)
        )

        validate_only_field = BooleanField(
            write_only=True, required=False, help_text="필드의 유효성 검사만을 수행합니다.",
        )
        serializer.fields["validate_only"] = validate_only_field
        return serializer
