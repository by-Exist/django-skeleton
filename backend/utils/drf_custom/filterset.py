from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet as OriginFilterSet
from django_filters import filters as django_filters  # has hint
from django_filters import rest_framework as filters  # not has hint


class FilterSet(OriginFilterSet):
    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        filter = super().filter_for_field(f, name, lookup_expr)
        filter.extra["help_text"] = f.help_text
        return filter
