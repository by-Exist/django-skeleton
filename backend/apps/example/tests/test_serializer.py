from dataclasses import dataclass
from django.test import TestCase
from .factories import CollectionFactory, NestedCollectionFactory, NestedResourceFactory
from ..serializers import (
    CollectionSerializer,
    NestedCollectionSerializer,
    NestedResourceSerializer,
    MoveNestedCollectionSerializer,
)


class CollectionSerializerTestCase(TestCase):
    def test_to_representation(self):
        collection = CollectionFactory()
        serializer = CollectionSerializer(collection)
        expected = {"id": collection.id, "title": collection.title}
        self.assertDictEqual(expected, serializer.data)

    def test_to_internal_value(self):
        data = {"title": "Title"}
        serializer = CollectionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(data, serializer.validated_data)


class NestedCollectionSerializerTestCase(TestCase):
    def test_to_representation(self):
        nested_collection = NestedCollectionFactory()
        serializer = NestedCollectionSerializer(nested_collection)
        expected = {
            "id": nested_collection.id,
            "title": nested_collection.title,
            "parent": nested_collection.parent.id,
        }
        self.assertDictEqual(expected, serializer.data)

    def test_to_internal_value(self):
        collection = CollectionFactory()

        @dataclass
        class ViewObj:
            kwargs: dict

        data = {"title": "Title"}
        view_obj = ViewObj(kwargs={"collection_pk": collection.id})
        serializer = NestedCollectionSerializer(data=data, context={"view": view_obj})
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(data, serializer.validated_data)


class MoveNestedCollectionSerializerTestCase(TestCase):
    def test_to_representation(self):
        nested_collection = NestedCollectionFactory()
        serializer = MoveNestedCollectionSerializer(nested_collection)
        expected = {
            "id": nested_collection.id,
            "title": nested_collection.title,
            "parent": nested_collection.parent.id,
        }
        self.assertDictEqual(expected, serializer.data)


class NestedResourceSerializerTestCase(TestCase):
    def test_to_representation(self):
        nested_resource = NestedResourceFactory()
        serializer = NestedResourceSerializer(nested_resource)
        expected = {
            "id": nested_resource.id,
            "title": nested_resource.title,
            "parent": nested_resource.parent.id,
        }
        self.assertDictEqual(expected, serializer.data)

    def test_to_internal_value(self):
        data = {"title": "Title"}
        serializer = NestedResourceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(data, serializer.validated_data)
