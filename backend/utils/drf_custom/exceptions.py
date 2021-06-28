from rest_framework import exceptions as rest_exceptions, status as rest_status


# ValidateOnlyGenericViewSetMixin
class PerformValidateOnly(rest_exceptions.APIException):
    status_code = rest_status.HTTP_204_NO_CONTENT
    default_detail = "perform validate only."
    default_code = "validate_only"


# ValidateOnlySerializerMixin
class BlockedSideEffect(rest_exceptions.APIException):
    status_code = rest_status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "validate_only 동작 수행에서 부작용이 있는 동작은 금지됩니다."
    default_code = "validate_only"
