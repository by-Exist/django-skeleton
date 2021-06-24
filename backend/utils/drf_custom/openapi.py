from drf_spectacular.extensions import OpenApiFilterExtension
from drf_spectacular.openapi import AutoSchema


class CustomAutoSchema(AutoSchema):
    def _get_filter_parameters(self):
        # filter_backends를 올바르게 불러오지 못하는 문제가 있어 수정
        # 단, view.filter_backends가 프로퍼티이며 filter_backends 또는 None 반환

        # if not self._is_list_view():
        #     return []
        if getattr(self.view, "filter_backends", None) is None:
            return []

        parameters = []
        for filter_backend in self.view.filter_backends:
            filter_extension = OpenApiFilterExtension.get_match(filter_backend())
            if filter_extension:
                parameters += filter_extension.get_schema_operation_parameters(self)
            else:
                parameters += filter_backend().get_schema_operation_parameters(
                    self.view
                )
        return parameters
