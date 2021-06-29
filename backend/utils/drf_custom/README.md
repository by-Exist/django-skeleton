# drf_custom

## [ 소개 ]

- django rest framework를 사용하면서 필요하다고 느꼈던 여러 추가적인 기능들이 구현되어 있습니다.
- 대부분의 기능들은 [Google API Design Guide](https://cloud.google.com/apis/design?hl=ko)에서 영감을 얻었습니다.

## [ 모듈 설명 ]

### exceptions.py

- drf-custom에서 활용되는 몇 가지 Exception이 담겨있는 모듈입니다.

### filters.py

- OrderingFilterBackend
  - "-id" 형식이 아닌 "id desc" 형식의 파라미터를 받습니다.
  - get_schema_operation_parameters가 더 많은 정보를 포함할 수 있도록 하였습니다.
- BatchGetFilterBackend
  - 커스텀메서드 [batchGet](https://cloud.google.com/apis/design/custom_methods?hl=ko#common_custom_methods)에서 활용됩니다.
- PathVariableFilterBackend
  - 와일드카드를 허용하는 url에서 사용될 필터 백엔드입니다.
  - CheckPathVariableViewSetMixin과 연관되어 있습니다.

### filterset.py

- FilterSet
  - django-filter를 활용하기 쉬운 방식으로 조립해놓은 모듈입니다.

### mixins.py

- ListModelMixin
  - 페이지네이션을 처음부터 강제합니다. 응답의 구조 변경을 최소화하기 위함입니다.
- UpdateModelMixin, PartialUpdateModelMixin
  - 두 믹스인을 분리함으로써 Put, Patch 중 원하는 동작만을 추가할 수 있습니다.

### openapi.py

- drf-spectacular(api 문서 제작 라이브러리)
- CustomAutoSchema
  - filter_backends의 파라미터를 가져오는 과정에 이상이 있어 커스텀
  - 파라미터를 가져오는 과정에 validate_only 추가
  - get_pk_description 번역

### pagination.py

- 기본적으로 활용될 페이지네이션 클래스들이 정의되어 있습니다.

### routers.py

- NestedMixin
  - rest_framework_nested의 NestedMixin입니다.
- CustomMethodMixin
  - lookup_value를 "\[^/.\]"에서 "\[^/.:\]"로 변경하였습니다.
- nested_singleton_routes
  - 중첩된 리소스에서 활용될 라우트 리스트입니다.
- custom_routes
  - [커스텀 메서드](https://cloud.google.com/apis/design/custom_methods?hl=ko)에서 활용될 라우트 리스트입니다.
- custom_nested_singleton_routes
  - 중첩된 리소스가 커스텀 메서드를 지원해야 할 때 사용될 라우트 리스트입니다.
- 바로 활용할 수 있는 여러 Router 클래스가 정의되어 있습니다.

### serializers.py

- ValidateOnlySerializerMixin
  - validate_only 쿼리 파라미터가 true일 경우 PerformValidateOnly가 발생하며, is_valid 수행 이후 시리얼라이저의 save, create, update 동작이 금지됩니다.

### viewsets.py

- ValidateOnlyGenericViewSetMixin
  - validate_only 동작을 지원하도록 동적으로 validate only serializer class를 생성하여 활용합니다.
- CheckPathVariableViewSetMixin
  - List가 wildcard를 허용할 경우 Create에서 "-"를 받아 에러를 일으킵니다.
  - 이를 해결하기 위해 모든 엔드포인트에서 Path 변수를 판단하는 로직을 추가하였습니다.
