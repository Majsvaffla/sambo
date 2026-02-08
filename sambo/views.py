from django.http import HttpRequest, HttpResponse

from . import components


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(components.index_page(request))
