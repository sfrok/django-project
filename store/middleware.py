from django.utils.deprecation import MiddlewareMixin
from .data import HtmlPages

class HeaderInfo(MiddlewareMixin):
    def process_request(self, request):
        request.pages = HtmlPages
        request.line = request.POST.get('line', '') if request.method == 'POST' else ''
        return None
