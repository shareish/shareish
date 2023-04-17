from rest_framework.pagination import PageNumberPagination


class ActivePaginationClass(PageNumberPagination):
    page_size = 20


class MessagePaginationClass(PageNumberPagination):
    page_size = 15
