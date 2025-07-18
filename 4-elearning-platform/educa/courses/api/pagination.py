from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 10
    # defines the name for the query parameter to use for the page size
    page_size_query_param = 'page_size'
    max_page_size = 50

