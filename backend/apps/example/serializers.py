from rest_framework import serializers
from .models import Collection, NestedCollection, NestedResource


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = "__all__"


class NestedCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedCollection
        fields = "__all__"


class NestedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedResource
        fields = "__all__"
