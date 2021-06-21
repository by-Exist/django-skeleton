from rest_framework.decorators import MethodMapper
from django.forms.utils import pretty_name


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def action(
    methods=None,
    detail=None,
    custom_method=False,
    url_path=None,
    url_name=None,
    **kwargs
):
    """추가된 action 메서드를 커스텀 메서드로 선택할 수 있는 기능과 url_path를 camalCase로 변환해주는 기능이 추가되었다."""

    methods = ["get"] if (methods is None) else methods
    methods = [method.lower() for method in methods]

    assert detail is not None, "@action() missing required argument: 'detail'"

    if "name" in kwargs and "suffix" in kwargs:
        raise TypeError("`name` and `suffix` are mutually exclusive arguments.")

    def decorator(func):
        func.mapping = MethodMapper(func, methods)
        func.detail = detail
        func.url_name = url_name if url_name else func.__name__.replace("_", "-")
        func.kwargs = kwargs
        # here
        func.url_path = (
            to_camel_case(url_path) if url_path else to_camel_case(func.__name__)
        )
        func.custom_method = custom_method

        if "name" not in kwargs and "suffix" not in kwargs:
            func.kwargs["name"] = pretty_name(func.__name__)

        func.kwargs["description"] = func.__doc__ or None

        return func

    return decorator
