from rest_framework import pagination as rest_pagination


class PageNumberPaginationMixin:
    page_query_param = "page"
    page_size_query_param = "pageSize"

    page_query_description = "조회하려는 페이지 번호입니다."


class SmallPageNumberPagination(
    PageNumberPaginationMixin, rest_pagination.PageNumberPagination
):
    page_size = 10
    max_page_size = 100

    page_size_query_description = "페이지 크기를 조절합니다. (default=10, max=100)"


class MiddlePageNumberPagination(
    PageNumberPaginationMixin, rest_pagination.PageNumberPagination
):
    page_size = 50
    max_page_size = 500

    page_size_query_description = "페이지 크기를 조절합니다. (default=50, max=500)"


class LargePageNumberPagination(
    PageNumberPaginationMixin, rest_pagination.PageNumberPagination
):
    page_size = 100
    max_page_size = 1000

    page_size_query_description = "페이지 크기를 조절합니다. (default=100, max=1000)"
