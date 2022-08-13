from rest_framework.pagination import PageNumberPagination

class ActivePaginationClass(PageNumberPagination):
    page_size = 3