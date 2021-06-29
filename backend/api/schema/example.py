from django.conf import settings
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
)


# Fix settings
# =============================================================================
settings.SPECTACULAR_SETTINGS["TITLE"] = "API Example"
settings.SPECTACULAR_SETTINGS["VERSION"] = "1.0.0"
settings.SPECTACULAR_SETTINGS[
    "DESCRIPTION"
] = """
## [ 설명 ]
API 문서를 만들 때 참고 삼을 수 있는 기반 틀을 제공합니다.

해당 문서는 backend.apps.example Application과 연동되어 있습니다.

## [ 구현된 기능 ]

### \- Validate Only
Google Api Guide - [요청 유효성 검사](https://cloud.google.com/apis/design/design_patterns?hl=ko)를 참고하였습니다.

해당 기능은 부작용이 있는 작업에 한하여, 유효성 검사만을 수행하고자 할 때 사용됩니다.

해당 기능을 지원하는 endpoint는 validate_only query parameter를 허용합니다.

쿼리 스트링에 validate_only=true가 전달되면, 유효성 검사에 문제가 없을 경우 204 Response를 반환합니다.

대부분의 create, update 동작에 구현되어 있습니다.

자세한 구현 방식은 ValidateOnlyGenericViewSetMixin을 살펴보기 바랍니다.

### \- Custom Method
Google Api Guide - [커스텀 메서드](https://cloud.google.com/apis/design/custom_methods?hl=ko)를 참고하였습니다.

[표준 메서드](https://cloud.google.com/apis/design/standard_methods?hl=ko)로 구현하기 적절하지 않은 동작을 구현할 때 사용됩니다.

| Endpoint | Description |
| --- | --- |
| collections:batchGet | 리소스 식별자 목록을 활용하여 리소스 일괄 가져오기 |
| collections:search | 기존 collection get과는 다른 방식으로 리소스 가져오기  |
| collections/\{collection_pk\}/nested-collections/\{pk\}:move| 리소스의 위치 변경에 사용되는 엔드포인트 |

자세한 구현 방식은 CustomMethodMixin, custom_routes를 살펴보기 바랍니다.

### \- WildCard
Google Api Guide - [하위 컬렉션](https://cloud.google.com/apis/design/design_patterns?hl=ko)을 참고하였습니다.

종종, 상위 컬렉션의 식별자를 모르더라도 하위 컬렉션의 List, Retrieve를 활용할 수 있도록 와일드 카드 "-"를 사용할 수 있습니다.

ex) GET https://library.googleapis.com/v1/shelves/-/books?filter=xxx

ex) GET https://library.googleapis.com/v1/shelves/-/books/{id}

자세한 구현 방식은 CheckPathVariableViewSetMixin, PathVariableFilterBackend를 살펴보시기 바랍니다.

## [ 모델 정보 ]
### collections
루트에 위치한 컬렉션입니다.

서브 컬렉션으로 nested collection을 지닙니다.

서브 리소스로 nested resource를 지닙니다. 생명 주기를 함께 합니다.
### nested collections
parent로 collection을 지니는 nested collection입니다.

중첩의 깊이를 최소한으로 유지하는 것이 좋습니다.
### nested resource
생명 주기가 collection에 종속적인 리소스입니다.

Read, Update만을 지원합니다.
"""


# Collection Schemas
# =============================================================================
collection_list_description = """
리소스 목록을 획득합니다.

정렬 및 페이징 기능을 제공합니다.
"""
collection_list_schema = extend_schema(
    description=collection_list_description, summary="컬렉션 목록", tags=["collection"]
)

collection_create_description = """
리소스를 추가합니다.
"""
collection_create_schema = extend_schema(
    description=collection_create_description, summary="컬렉션 생성", tags=["collection"]
)

collection_retrieve_description = """
단일 리소스를 조회합니다.
"""
collection_retrieve_schema = extend_schema(
    description=collection_retrieve_description, summary="컬렉션 조회", tags=["collection"]
)

collection_partial_update_description = """
기존에 존재하는 리소스를 수정합니다.
"""
collection_partial_update_schema = extend_schema(
    description=collection_partial_update_description,
    summary="컬렉션 수정",
    tags=["collection"],
)

collection_destroy_description = """
리소스를 제거합니다.
"""
collection_destroy_schema = extend_schema(
    description=collection_destroy_description, summary="컬렉션 삭제", tags=["collection"]
)

collection_batch_get_description = """
pk를 활용하여 일괄적으로 리소스들을 가져옵니다.
"""
collection_batch_get_schema = extend_schema(
    description=collection_batch_get_description,
    summary="컬렉션 일괄 목록",
    tags=["collection"],
)

collection_search_description = """
list와는 다른 방식으로 리소스 목록을 조회합니다.
"""
collection_search_schema = extend_schema(
    description=collection_search_description,
    summary="컬렉션 다른 방식의 조회",
    tags=["collection"],
)


class FixCollectionViewSet(OpenApiViewExtension):
    target_class = "apps.example.views.CollectionViewSet"

    def view_replacement(self):
        FixedViewSet = extend_schema_view(
            list=collection_list_schema,
            create=collection_create_schema,
            retrieve=collection_retrieve_schema,
            partial_update=collection_partial_update_schema,
            destroy=collection_destroy_schema,
            batch_get=collection_batch_get_schema,
            search=collection_search_schema,
        )(self.target_class)
        return FixedViewSet


# Nested Collection Schemas
# =============================================================================
nested_collection_list_description = """
리소스 목록을 획득합니다.

정렬 및 페이징 기능을 제공합니다.
"""
nested_collection_list_schema = extend_schema(
    description=nested_collection_list_description,
    summary="중첩 컬렉션 목록",
    tags=["nested collection"],
)

nested_collection_create_description = """
리소스를 추가합니다.
"""
nested_collection_create_schema = extend_schema(
    description=nested_collection_create_description,
    summary="중첩 컬렉션 생성",
    tags=["nested collection"],
)

nested_collection_retrieve_description = """
단일 리소스를 조회합니다.
"""
nested_collection_retrieve_schema = extend_schema(
    description=nested_collection_retrieve_description,
    summary="중첩 컬렉션 조회",
    tags=["nested collection"],
)

nested_collection_partial_update_description = """
기존에 존재하는 리소스를 수정합니다.
"""
nested_collection_partial_update_schema = extend_schema(
    description=nested_collection_partial_update_description,
    summary="중첩 컬렉션 수정",
    tags=["nested collection"],
)

nested_collection_destroy_description = """
리소스를 제거합니다.
"""
nested_collection_destroy_schema = extend_schema(
    description=nested_collection_destroy_description,
    summary="중첩 컬렉션 삭제",
    tags=["nested collection"],
)

nested_collection_move_description = """
리소스의 이동 작업(url의 변동)은 put이나 patch가 아닌 별도의 엔드포인트로 처리합니다.

해당 리소스를 다른 상위 리소스로 이동합니다.
"""
nested_collection_move_schema = extend_schema(
    description=nested_collection_move_description,
    summary="중첩 컬렉션 이동",
    tags=["nested collection"],
)


class FixCollectionViewSet(OpenApiViewExtension):
    target_class = "apps.example.views.NestedCollectionViewSet"

    def view_replacement(self):
        FixedViewSet = extend_schema_view(
            list=nested_collection_list_schema,
            create=nested_collection_create_schema,
            retrieve=nested_collection_retrieve_schema,
            partial_update=nested_collection_partial_update_schema,
            destroy=nested_collection_destroy_schema,
            move=nested_collection_move_schema,
        )(self.target_class)
        return FixedViewSet


# Collection Schemas
# =============================================================================
nested_resource_retrieve_description = """
리소스의 정보를 조회합니다.
"""
nested_resource_retrieve_schema = extend_schema(
    description=nested_resource_retrieve_description,
    summary="리소스 조회",
    tags=["nested resource"],
)

nested_resource_partial_update_description = """
기존에 존재하는 리소스를 수정합니다.
"""
nested_resource_partial_update_schema = extend_schema(
    description=nested_resource_partial_update_description,
    summary="리소스 수정",
    tags=["nested resource"],
)


class FixCollectionViewSet(OpenApiViewExtension):
    target_class = "apps.example.views.NestedResourceViewSet"

    def view_replacement(self):
        FixedViewSet = extend_schema_view(
            retrieve=nested_resource_retrieve_schema,
            partial_update=nested_resource_partial_update_schema,
        )(self.target_class)
        return FixedViewSet

