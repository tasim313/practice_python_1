from rest_framework import pagination


class StandardResultsSetPagination(pagination.PageNumberPagination):

    """
    Naznin: This is for pagination. Here we can change page_size number as we want to see.
    """

    page_size = 10
    page_size_query_param = 'page_size'