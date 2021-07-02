from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import CollectionFactory, NestedCollectionFactory, NestedResourceFactory


class CollectionViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.collection = CollectionFactory()
        self.collections = CollectionFactory.create_batch(10)
        self.valid_data = {"title": "유효한 값"}
        self.invalid_data = {"title": "유효하지 않은 값, 스무 글자 이상 기록할 수 없습니다."}

    def test_list(self):
        url = reverse("collection-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_ordering(self):
        url = reverse("collection-list")
        desc_response = self.client.get(url, {"ordering": "title desc"})
        asc_response = self.client.get(url, {"ordering": "title"})
        self.assertNotEqual(asc_response.data["results"], desc_response.data["results"])
        desc_response = self.client.get(url, {"ordering": "id desc"})
        asc_response = self.client.get(url, {"ordering": "id"})
        self.assertNotEqual(asc_response.data["results"], desc_response.data["results"])

    def test_list_paging(self):
        url = reverse("collection-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("count" in response.data, True)
        self.assertEqual("next" in response.data, True)
        self.assertEqual("previous" in response.data, True)
        self.assertEqual("results" in response.data, True)

    def test_create(self):
        url = reverse("collection-list")
        response = self.client.post(url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(self.valid_data, response.data)

    def test_create_validate_only(self):
        url = reverse("collection-list")
        response = self.client.post(f"{url}?validate_only=true", self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post(f"{url}?validate_only=true", self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        url = reverse("collection-detail", kwargs={"pk": self.collection.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"id": self.collection.id, "title": self.collection.title}
        )

    def test_partial_update(self):
        url = reverse("collection-detail", kwargs={"pk": self.collection.id})
        update_data = {"title": "바뀐 제목"}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(update_data, response.data)

    def test_partial_update_validate_only(self):
        url = reverse("collection-detail", kwargs={"pk": self.collection.id})
        response = self.client.patch(f"{url}?validate_only=true", self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.patch(f"{url}?validate_only=true", self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        url = reverse("collection-detail", kwargs={"pk": self.collection.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_batch_get(self):
        collection_pk_list = [collection.id for collection in self.collections]
        valueList = ",".join(str(pk) for pk in collection_pk_list)
        url = reverse("collection-batch-get")
        res = self.client.get(f"{url}?valueList={valueList}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        results_ids = [collection["id"] for collection in res.data["results"]]
        self.assertEqual(set(results_ids).issubset(set(collection_pk_list)), True)

    def test_batch_get_ordering(self):
        collection_pk_list = [collection.id for collection in self.collections]
        valueList = ",".join(str(pk) for pk in collection_pk_list)
        url = reverse("collection-batch-get")
        res_1 = self.client.get(f"{url}?valueList={valueList}&ordering=id")
        res_2 = self.client.get(f"{url}?valueList={valueList}&ordering=id desc")
        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res_1.data["results"], res_2.data["results"])

    def test_search(self):
        url = reverse("collection-search")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_search_ordering(self):
        url = reverse("collection-search")
        res_1 = self.client.get(f"{url}?ordering=id")
        res_2 = self.client.get(f"{url}?ordering=id desc")
        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res_1.data["results"], res_2.data["results"])

    def test_search_filtering(self):
        collection_1 = CollectionFactory(title="전체여부")
        collection_2 = CollectionFactory(title="포함여부를 확인합니다.")
        url = reverse("collection-search")
        res = self.client.get(f"{url}?title=전체여부")
        self.assertEqual(res.data["results"][0]["id"], collection_1.id)
        res = self.client.get(f"{url}?title__contains=포함여부")
        self.assertEqual(res.data["results"][0]["id"], collection_2.id)


class NestedCollectionViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.some_parent = CollectionFactory()
        self.nested_collection = NestedCollectionFactory()
        self.nested_collections = NestedCollectionFactory.create_batch(10)
        self.valid_data = {"title": "유효한 제목입니다."}
        self.invalid_data = {"title": "유효하지 않은 임의의 길이를 지닌 제목입니다."}
        self.move_valid_data = {"parent": self.some_parent.pk}
        self.move_invalid_data = {"parent": 99999}

    def test_list(self):
        url = reverse(
            "nested-collection-list",
            kwargs={"collection_pk": self.nested_collection.parent.pk},
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_wildcard(self):
        url = reverse("nested-collection-list", kwargs={"collection_pk": "-"})
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_ordering(self):
        collection = CollectionFactory()
        for _ in range(10):
            NestedCollectionFactory(parent=collection)
        url = reverse("nested-collection-list", kwargs={"collection_pk": "-"})
        asc_res = self.client.get(f"{url}?ordering=id")
        desc_res = self.client.get(f"{url}?ordering=id desc")
        self.assertEqual(asc_res.status_code, status.HTTP_200_OK)
        self.assertEqual(desc_res.status_code, status.HTTP_200_OK)
        self.assertEqual(asc_res.data["results"] != desc_res.data["results"], True)

    def test_list_paging(self):
        url = reverse(
            "nested-collection-list", kwargs={"collection_pk": self.some_parent.id}
        )
        res = self.client.get(url)
        self.assertEqual("count" in res.data, True)
        self.assertEqual("next" in res.data, True)
        self.assertEqual("previous" in res.data, True)
        self.assertEqual("results" in res.data, True)

    def test_create(self):
        url = reverse(
            "nested-collection-list", kwargs={"collection_pk": self.some_parent.id}
        )
        res = self.client.post(url, self.valid_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.post(url, self.invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_validate_only(self):
        url = reverse(
            "nested-collection-list", kwargs={"collection_pk": self.some_parent.id}
        )
        res = self.client.post(f"{url}?validate_only=true", self.valid_data)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.post(f"{url}?validate_only=true", self.invalid_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        url = reverse(
            "nested-collection-detail",
            kwargs={
                "collection_pk": self.nested_collection.parent.pk,
                "pk": self.nested_collection.pk,
            },
        )
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_wildcard(self):
        url_1 = reverse(
            "nested-collection-detail",
            kwargs={
                "collection_pk": self.nested_collection.parent.pk,
                "pk": self.nested_collection.pk,
            },
        )
        url_2 = reverse(
            "nested-collection-detail",
            kwargs={"collection_pk": "-", "pk": self.nested_collection.pk,},
        )
        res_1 = self.client.get(url_1)
        res_2 = self.client.get(url_2)
        self.assertEqual(res_1.data, res_2.data)

    def test_partial_update(self):
        url = reverse(
            "nested-collection-detail",
            kwargs={
                "collection_pk": self.nested_collection.parent.pk,
                "pk": self.nested_collection.pk,
            },
        )
        origin_title = self.nested_collection.title
        res = self.client.patch(url, self.valid_data)
        self.assertNotEqual(res.data["title"], origin_title)

    def test_partial_update_validate_only(self):
        url = reverse(
            "nested-collection-detail",
            kwargs={
                "collection_pk": self.nested_collection.parent.pk,
                "pk": self.nested_collection.pk,
            },
        )
        res = self.client.patch(f"{url}?validate_only=true", self.valid_data)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy(self):
        url = reverse(
            "nested-collection-detail",
            kwargs={
                "collection_pk": self.nested_collection.parent.id,
                "pk": self.nested_collection.id,
            },
        )
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_move(self):
        url = reverse(
            "nested-collection-move",
            kwargs={
                "collection_pk": self.nested_collection.parent.id,
                "pk": self.nested_collection.id,
            },
        )
        origin_parent_id = self.nested_collection.parent.id
        res = self.client.post(url, self.move_valid_data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(origin_parent_id, res.data["parent"])

    def test_move_validate_only(self):
        url = reverse(
            "nested-collection-move",
            kwargs={
                "collection_pk": self.nested_collection.parent.id,
                "pk": self.nested_collection.id,
            },
        )
        origin_parent_id = self.nested_collection.parent.id
        validate_res = self.client.post(
            f"{url}?validate_only=true", self.move_valid_data
        )
        self.assertEqual(validate_res.status_code, status.HTTP_204_NO_CONTENT)
        invalidate_res = self.client.post(
            f"{url}?validate_only=true", self.move_invalid_data
        )
        self.assertEqual(invalidate_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(origin_parent_id, self.nested_collection.parent.pk)


class NestedResourceViewSetTestCase(APITestCase):
    def setUp(self) -> None:
        self.nested_resource = NestedResourceFactory()
        self.collection = self.nested_resource.parent
        self.validate_data = {"title": "유효한 값입니다."}
        self.invalidate_data = {"title": "유효하지 않은 길의의 제목입니다. (20글자)"}

    def test_created(self):
        collection_url = reverse("collection-list")
        collection_res = self.client.post(collection_url, {"title": "제목입니다"})
        collection_id = collection_res.data["id"]
        nested_resource_url = reverse(
            "nested-resource-detail", kwargs={"collection_pk": collection_id}
        )
        nested_resource_res = self.client.get(nested_resource_url)
        self.assertEqual(nested_resource_res.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        pass

    def test_partial_update(self):
        pass

    def test_partial_update_validate_only(self):
        pass

    def test_deleted(self):
        collection_url = reverse("collection-list")
        collection_res = self.client.post(collection_url, {"title": "제목입니다"})
        self.assertEqual(collection_res.status_code, status.HTTP_201_CREATED)
        collection_id = collection_res.data["id"]
        collection_detail_url = reverse(
            "collection-detail", kwargs={"pk": collection_id}
        )
        collection_res = self.client.delete(collection_detail_url)
        self.assertEqual(collection_res.status_code, status.HTTP_204_NO_CONTENT)
        nested_resource_url = reverse(
            "nested-resource-detail", kwargs={"collection_pk": collection_id}
        )
        nested_resource_res = self.client.get(nested_resource_url)
        self.assertEqual(nested_resource_res.status_code, status.HTTP_404_NOT_FOUND)
