from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """Стандартный пагинатор."""
    page_size_query_param = 'limit'
