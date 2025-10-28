from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class limiting results per page to 6 by default.
    Supports custom page size up to a maximum of 100 via query parameter.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100