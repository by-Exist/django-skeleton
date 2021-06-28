from django.shortcuts import get_object_or_404
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
        read_only_fields = ["parent"]

    def validate(self, attrs):
        collection_pk: str = self.context["view"].kwargs["collection_pk"]
        collection = get_object_or_404(Collection, pk=collection_pk)
        if NestedCollection.objects.filter(
            parent=collection, title=attrs["title"]
        ).exists():
            raise serializers.ValidationError(
                detail={
                    "title": "collection에 이미 해당 title의 nested collection 리소스가 존재합니다."
                }
            )
        return attrs


class MoveNestedCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedCollection
        fields = "__all__"
        read_only_fields = ["title"]


class NestedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedResource
        fields = "__all__"
        read_only_fields = ["parent"]
