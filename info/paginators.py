from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    page_size = 3  # Количество элементов на странице
    page_size_query_param = (
        "page_size"  # Параметр запроса для указания количества элементов на странице
    )
