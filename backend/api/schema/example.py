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
## Intro
API 문서를 만들 때 참고 삼을 수 있는 기반 틀을 제공합니다.

해당 문서는 backend.apps.example app과 연동되어 있습니다. 실제 구현 방식은 코드를 살펴보기 바랍니다.

## Validate Only
해당 기능은 부작용이 있는 작업에 한하여, 유효성 검사만을 진행하고자 할 때 사용됩니다.

쿼리 스트링으로 validate_only=true를 전달받음으로써 수행되며, 유효성 검사에 문제가 없을 경우 status code 204인 빈 Response를 반환합니다.

해당 기능을 지원하는 endpoint는 validate_only parameter가 추가됩니다.

## Group info
### collections
Create, Read, Update, Delete를 지원하는 루트 컬렉션입니다.

권장되는 형태의 엔드포인트입니다.
### nested collections
Create, Read, Update, Delete를 지원하며, 상위 리소스에 종속적인 컬렉션입니다.

중첩의 깊이가 2단계 이상 깊어지지 않도록 하십시오. 자원 간의 관계가 직관적이지 않습니다.

만약 url을 통해 노출하고 싶지 않은 정보가 포함된다면 중첩 관계를 제거한 루트 컬렉션으로 활용하세요.
### nested resource
생명 주기가 상위 리소스에 종속적인 리소스입니다.

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

