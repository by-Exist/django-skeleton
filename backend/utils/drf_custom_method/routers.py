from rest_framework.routers import SimpleRouter, DefaultRouter
from .mixins import CustomMethodMixin, NestedMixin
from .routes import custom_method_default_routes, sub_resource_singleton_routes


# Custom Method
# =============================================================================
class CustomMethodSimpleRouter(CustomMethodMixin, SimpleRouter):
    """
    CustomMethod 동작을 지원하는 SimpleRouter

    [Google API Guide - CustomMethod](https://cloud.google.com/apis/design/custom_methods?hl=ko)

    action.custom_method 속성을 읽어야 하기 때문에 drf_custom_method.decorators의 custom_action에 종속적이다.

    lookup_value_regex가 [^/.]에서 [^/.:]로 변경된다.
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다.
    """

    routes = custom_method_default_routes


class CustomMethodDefaultRouter(CustomMethodMixin, DefaultRouter):
    """
    CustomMethod 동작을 지원하는 DefaultRouter

    [Google API Guide - CustomMethod](https://cloud.google.com/apis/design/custom_methods?hl=ko)

    action.custom_method 속성을 읽어야 하기 때문에 drf_custom_method.decorators의 custom_action에 종속적이다.

    lookup_value_regex가 [^/.]에서 [^/.:]로 변경된다.
    
    pk에 슬래시(/), 점(.), 콜론(:)이 포함될 경우 viewset의 lookup_value_regex를 재정의하여야 한다.
    """

    routes = custom_method_default_routes


# Nested + Custom Method
# =============================================================================
class NestedCustomMethodSimpleRouter(NestedMixin, CustomMethodSimpleRouter):
    """
    CustomMethod 동작을 지원하는 NestedSimpleRouter
    """

    routes = custom_method_default_routes


class NestedCustomMethodDefaultRouter(NestedMixin, CustomMethodDefaultRouter):
    """
    CustomMethod 동작을 지원하는 NestedDefaultRouter
    """

    routes = custom_method_default_routes


# Nested + Custom Method + Singleton Resource
# =============================================================================
class NestedSingletonResourceCustomMethodSimpleRouter(NestedCustomMethodSimpleRouter):
    """
    CustomMethod 동작을 지원하며 리소스가 싱글 톤일 때 활용되는 NestedSimpleRouter
    """

    routes = sub_resource_singleton_routes


class NestedSingletonResourceCustomMethodDefaultRouter(NestedCustomMethodDefaultRouter):
    """
    CustomMethod 동작을 지원하며 리소스가 싱글 톤일 때 활용되는 NestedDefaultRouter
    """

    routes = sub_resource_singleton_routes
