from rest_framework import pagination
from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound


class SmallPageNumberPagination(pagination.PageNumberPagination):

    page_size = 100
    max_page_size = 500

    page_query_param = "page"
    page_query_description = "A page number within the paginated result set."

    page_size_query_param = "page-size"
    page_size_query_description = "Number of results to return per page."

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class MediumPageNumberPagination(pagination.PageNumberPagination):

    page_size = 500
    max_page_size = 1000

    page_query_param = "page"
    page_query_description = "A page number within the paginated result set."

    page_size_query_param = "page-size"
    page_size_query_description = "Number of results to return per page."


class LargePageNumberPagination(pagination.PageNumberPagination):

    page_size = 1000
    max_page_size = 5000

    page_query_param = "page"
    page_query_description = "A page number within the paginated result set."

    page_size_query_param = "page-size"
    page_size_query_description = "Number of results to return per page."

