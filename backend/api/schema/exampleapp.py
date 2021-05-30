from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema, extend_schema_view


# Tag
tags = ["examples"]

# List
list_summary = "목록"
list_schema = extend_schema(tags=tags, summary=list_summary)

# Create
create_summary = "생성"
create_schema = extend_schema(tags=tags, summary=create_summary)

# Retrieve
retrieve_summary = "정보"
retrieve_schema = extend_schema(tags=tags, summary=retrieve_summary)

# Update
update_summary = "교체"
update_schema = extend_schema(tags=tags, summary=update_summary)

# Partial_update
partial_update_summary = "수정"
partial_update_schema = extend_schema(tags=tags, summary=partial_update_summary)

# Destroy
destroy_summary = "삭제"
destroy_schema = extend_schema(tags=tags, summary=destroy_summary)

# Collection Custom Method
collection_custom_method_summary = "컬렉션 커스텀 메소드"
collection_custom_method_schema = extend_schema(
    tags=tags, summary=collection_custom_method_summary
)

# Resource Custom Method
resource_custom_method_summary = "리소스 커스텀 메소드"
resource_custom_method_schema = extend_schema(
    tags=tags, summary=resource_custom_method_summary
)


class ExampleExtension(OpenApiViewExtension):
    target_class = "apps.exampleapp.views.ExampleViewSet"

    def view_replacement(self):
        FixedViewSet = extend_schema_view(
            list=list_schema,
            create=create_schema,
            retrieve=retrieve_schema,
            update=update_schema,
            partial_update=partial_update_schema,
            destroy=destroy_schema,
            collection_custom_method=collection_custom_method_schema,
            resource_custom_method=resource_custom_method_schema,
        )(self.target_class)
        return FixedViewSet
