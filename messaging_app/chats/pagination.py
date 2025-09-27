# messaging_app/chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        total_count = self.page.paginator.count
        page_number = self.page.number
        total_pages = self.page.paginator.num_pages

        return Response({
            "count": total_count,
            "page_number": page_number,
            "total_pages": total_pages,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
