from utils.drf_custom.filterset import FilterSet
from .models import Collection, NestedCollection, NestedResource

# from utils.drf_custom.filterset import django_filters as filters  # use write (has hint)
from utils.drf_custom.filterset import filters  # use run (not has hint)


class NumberRangeFilter(filters.BaseRangeFilter, filters.NumberFilter):
    pass


class CollectionFilter(FilterSet):

    title = filters.CharFilter()
    title__contains = filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="titleContains"
    )

    class Meta:
        model = Collection
        fields = ["title", "title__contains"]
