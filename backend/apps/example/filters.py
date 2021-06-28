from utils.drf_custom.filterset import FilterSet
from .models import Collection, NestedCollection, NestedResource

# from utils.drf_custom.filterset import django_filters as filters  # use write (has hint)
from utils.drf_custom.filterset import filters  # use run (not has hint)


class NumberRangeFilter(filters.BaseRangeFilter, filters.NumberFilter):
    pass


class CollectionFilter(FilterSet):

    title = filters.CharFilter(help_text="title과 일치하는 Collection을 조회합니다.")
    title__contains = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text="title 내에 문자열이 포함된 Collection을 조회합니다.",
    )

    class Meta:
        model = Collection
        fields = ["title", "title__contains"]
