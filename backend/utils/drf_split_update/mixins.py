from rest_framework.mixins import UpdateModelMixin


class OnlyUpdateModelMixin:
    """rest_framework.mixins의 update 동작만을 제공하는 믹스인"""

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = False
        return UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()


class OnlyPartialUpdateMixin:
    """rest_framework.mixins의 partial_update 동작만을 제공하는 믹스인"""

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return UpdateModelMixin.update(self, request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
