# Custom DRF

- 기존 rest framework에서 몇 가지 기능이 추가되었습니다.
  - rest_framework.mixins
  - rest_framework.decorators
  - rest_framework.routers
  - rest_framework.viewsets

## 기능 요약

- custom_drf.mixins
  - ReplaceModelMixin, ModifyModelMixin 추가
  - validate_only 동작 지원 추가 (Replace, Modify, Create)
  - List 믹스인의 pagination 동작 강제

- custom_drf.decorators
  - custom_drf.routers에 정의된 라우터가 의존하고 있는 action 데코레이터 정의
  - custom_method 파라미터가 추가됨

- custom_drf.routers
  - [Custom Method](https://cloud.google.com/apis/design/custom_methods?hl=ko) 기능을 지원하는 라우터 추가

- custom_drf.viewsets
  - serializer에 validate_only 필드를 동적으로 추가

## 기능 상세

### custom_drf.mixins

- UpdateModelMixin(patch, put) => ReplaceModelMixin(put), ModifyModelMixin(patch)
  - 두 개의 메소드를 별도로 활용하기 위해 Update를 Replace, Modify로 나누었다.

- validate_only 기능을 추가하였다.
  - 설명
    - body가 있는 메서드(post, put, patch)에 한하여
    - 필드의 유효성 검사만을 수행하는 validate_only 기능을 추가하였다.
    - 이는 서버에 부작용(데이터 변경)을 일으켜서는 안된다.
    - ValidationError가 발생하지 않는다면 HTTP_204_OK를 응답한다.
    - HTTP_204_OK를 응답받은 동일한 요청이 ValidationError가 발생하면 안된다.
    - 기타 에러는 발생할 수 있다.
  - mixins
    - serializer.is_valide(raise_exception=True)를 거친 후
    - serializer.validate_data.get('validate_only', False)의 값이 True일 경우
    - perform_... 로직을 거치지 않고 바로 204 응답을 반환하는 것으로 구현된다.
      - perform_create, perform_replace, perform_modify

- ListSerializer의 Pagination 기능을 강제하였다.
  - Google api 가이드에서, response의 형식이 달라지기 때문에 작은 사이즈더라도 페이징을 처음부터 사용하도록 권고하고 있다.
  - 만약 ListModelMixin이 활용되었으며 pagination_class이 정의되지 않았을 경우
  - custom_drf.mixins.PaginationClassNotFoundException이 발생한다.

### custom_drf.decorators

- action
  - action으로 데코레이팅 된 view 함수의 어트리뷰트에 custom_method(bool)을 추가하는 방식으로 구현되어 있다.
    - [Google API Guide - Custom Method](https://cloud.google.com/apis/design/custom_methods?hl=ko)를 참고로 해당 기능을 지원하기 위해 기존 action 기능에 파라미터를 추가하였다.
    - 해당 어트리뷰트는 router에서 활용된다.
  - custom_method는 patch 사용 불가
    - patch이면서 custom_method가 True일 경우 Assertion을 발생시킨다.

### custom_drf.routers

- routes
  - Route, DynamicRoute의 url에서 사용된 url과 action의 구분자 /를 {slash}로 변경
  - nestedsingletonroutes
    - 의도적으로 create, delete 매핑이 제거되어 있다.
    - 해당 리소스의 생성/제거는 상위 리소스와 연동되어 있기 때문.
- routers
  - [Google API Guide - Custom Method](https://cloud.google.com/apis/design/custom_methods?hl=ko)를 참고로 해당 기능을 지원하기 위해 기존 router 기능을 수정하였다.
    - _get_dynamic_route = view의 custom_method가 True일 경우
      - target/action이 아닌 target:action 형식으로 Route로 변환하도록 설정
    - get_lookup_regex = lookup_value_regex를 [^/.]+에서 [^/.:]+로 변경
      - 그러므로, 만약 pk에 : 문자열이 포함될 가능성이 있을 경우 lookup_value_regex를 적절하게 설정해주어야 한다.
  - NestedCustomMethodRouter
    - rest_framework_nested.routers의 NestedMixin을 활용하였다.

### custom_drf.viewset

- viewsets.ValidateOnlyMixin
  - get_serializer를 오버라이트하여 작성되었다.
    - 만약 viewset 클래스 변수로 validate_only_actions가 정의되어 있고
      - create(post), replace(put), modify(patch)만 포함될 수 있다.
      - 허용되지 않은 메서드는 AssertionError를 발생시킨다.
    - action이 validate_only_actions에 포함되어 있다면
    - serializer에 validate_only 필드를 동적으로 추가한다.
