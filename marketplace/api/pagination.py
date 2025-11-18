from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 500
    limit_query_param = 'limit'
    offset_query_param = 'offset'
