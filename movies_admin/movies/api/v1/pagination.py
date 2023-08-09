from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FilmworkPagination(PageNumberPagination):

    page_size = 50

    def get_paginated_response(self, data):
        total_pages = round(self.page.paginator.count / self.page_size)
        previous_page = (
            self.page.previous_page_number()
            if self.page.number > 1 else None
        )
        next_page = (
            self.page.next_page_number()
            if self.page.number < total_pages else None
        )
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('total_pages', total_pages),
            ('prev', previous_page),
            ('next', next_page),
            ('results', data)
        ]))
