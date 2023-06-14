from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict

class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10
    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('lastPage', self.page.paginator.count),
             ('countItemsOnPage', self.page_size),
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('results', data)
         ]))

class CustomPaginationWithFile(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10
    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('lastPage', self.page.paginator.count),
             ('countItemsOnPage', self.page_size),
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('filename', str(self.request.FILES.get('file_uploaded'))),
             ('results', data)
         ]))
