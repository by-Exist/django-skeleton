from django.test import TestCase
from django.db import models
from ..models import Collection, NestedCollection, NestedResource


class CollectionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Collection.objects.create(title="테스트에 사용되는 Collection")

    # field
    def test_title_verbose_name(self):
        collection = Collection.objects.first()
        title_field_verbose_name = collection._meta.get_field("title").verbose_name
        self.assertEqual(title_field_verbose_name, "제목")

    def test_title_max_length(self):
        collection = Collection.objects.first()
        title_field_max_length = collection._meta.get_field("title").max_length
        self.assertEqual(title_field_max_length, 20)


class NestedCollectionTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        collection = Collection.objects.create(title="테스트 Collection")
        NestedCollection.objects.create(parent=collection, title="테스트 NestedCollection")

    def test_meta_ordering(self):
        self.assertEqual(NestedCollection._meta.ordering, ["-id"])

    def test_meta_unique_together(self):
        self.assertEqual(NestedCollection._meta.unique_together, (("parent", "title"),))

    def test_field_parent_related_name(self):
        collection = Collection.objects.first()
        nested_collection = NestedCollection.objects.first()
        self.assertEqual(nested_collection.parent, collection)

    def test_field_parent_reverse_related_name(self):
        collection = Collection.objects.first()
        nested_collection = NestedCollection.objects.first()
        self.assertEqual(collection.nestedcollection_set.first(), nested_collection)

    def test_field_parent_on_delete_is_cascade(self):
        self.assertEqual(
            NestedCollection._meta.get_field("parent").remote_field.on_delete,
            models.CASCADE,
        )

    def test_field_title_max_length(self):
        title_max_length = NestedCollection._meta.get_field("title").max_length
        self.assertEqual(title_max_length, 20)


class NestedResourceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        collection = Collection.objects.create(title="테스트 Collection")
        NestedResource.objects.create(parent=collection, title="테스트 Nested Resource")

    def test_meta_ordering(self):
        self.assertEqual(NestedResource._meta.ordering, ["-id"])

    def test_field_parent_on_delete_is_cascade(self):
        self.assertEqual(
            NestedResource._meta.get_field("parent").remote_field.on_delete,
            models.CASCADE,
        )

    def test_field_parent_related_name(self):
        collection = Collection.objects.first()
        nested_resource = NestedResource.objects.first()
        self.assertEqual(collection.child, nested_resource)

    def test_field_parent_reverse_related_name(self):
        collection = Collection.objects.first()
        nested_resource = NestedResource.objects.first()
        self.assertEqual(nested_resource.parent, collection)

    def test_field_title_max_length(self):
        title_field = NestedResource._meta.get_field("title")
        self.assertEqual(title_field.max_length, 20)
