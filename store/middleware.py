from django.utils.deprecation import MiddlewareMixin
from .data import HtmlPages
from .settings import APP_NAME

class HeaderInfo(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        request.pages = HtmlPages
        request.line = request.POST.get('line', '') if request.method == 'POST' else ''
        request.name = APP_NAME
        return None
