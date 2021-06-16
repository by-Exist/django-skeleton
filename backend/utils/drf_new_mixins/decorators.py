from rest_framework.decorators import MethodMapper, pretty_name
from rest_framework.decorators import action as rest_action


def action(
    methods=None,
    detail=None,
    custom_method=False,
    url_path=None,
    url_name=None,
    **kwargs
):
    # 기존 action에서 custom_method 파라미터를 추가하였다.
    origin_decorator = rest_action(methods, detail, url_path, url_name, **kwargs)

    def decorator(func):
        func = origin_decorator(func)
        func.custom_method = custom_method
        return func

    return decorator
