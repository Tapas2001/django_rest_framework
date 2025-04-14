from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# for custome pagination for employee view
class CustomePagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page-num' # ex - ?page-num=2 # if put only page then ?page=2 and if not set the attribute take default result is ?page=2, here put any thing you want other wise it take page as default
    max_page_size = 1

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data # here  data is serialized data
        })