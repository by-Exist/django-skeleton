from rest_framework.decorators import MethodMapper, pretty_name


def action(
    methods=None,
    detail: bool = None,
    # here
    custom_method: bool = False,
    url_path: str = None,
    url_name: str = None,
    **kwargs
):
    """
    rest_framework.decorators의 action 함수를 확장한 데코레이터

    custom_method 인자가 추가되었다

    해당 인자의 값은 drf_custom_method.routers의 CustomMethodRouter에서 활용된다
    """
    methods = ["get"] if (methods is None) else methods
    methods = [method.lower() for method in methods]

    assert detail is not None, "@action() missing required argument: 'detail'"
    assert (
        custom_method is True and "patch" not in methods
    ), "HTTP method PATCH는 커스텀 메소드로 사용할 수 없습니다."

    if "name" in kwargs and "suffix" in kwargs:
        raise TypeError("`name` and `suffix` are mutually exclusive arguments.")

    def decorator(func):
        func.mapping = MethodMapper(func, methods)

        func.detail = detail
        func.url_path = url_path if url_path else func.__name__
        func.url_name = url_name if url_name else func.__name__.replace("_", "-")
        # here
        func.custom_method = custom_method
        func.kwargs = kwargs

        if "name" not in kwargs and "suffix" not in kwargs:
            func.kwargs["name"] = pretty_name(func.__name__)
        func.kwargs["description"] = func.__doc__ or None

        return func

    return decorator
