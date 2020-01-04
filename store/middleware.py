from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from .data import HtmlPages
from .settings import APP_NAME


class HeaderInfo(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        request.pages = HtmlPages
        request.line = request.POST.get('line', '') if request.method == 'POST' else ''
        request.name = APP_NAME
        return None


class AdminAccess(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        if request.path[:5] == '/gts/' and request.user.is_staff is False:
            raise Http404
        return None
