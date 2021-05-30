from rest_framework import mixins, viewsets, response, status
from drf_custom_method.decorators import slash_editable_action
from .models import Example
from .serializers import ExampleSerializer


class ExampleViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer

    @slash_editable_action(methods=["post"], detail=False, slash=":")
    def collection_custom_method(self, request, *args, **kwargs):
        return response.Response(data={}, status=status.HTTP_201_CREATED)

    @slash_editable_action(methods=["post"], detail=True, slash=":")
    def resource_custom_method(self, request, pk=None, *args, **kwargs):
        return response.Response(data={}, status=status.HTTP_201_CREATED)
