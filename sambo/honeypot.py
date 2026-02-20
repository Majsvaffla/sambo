import typing as t

from django.http import HttpRequest, HttpResponse

if t.TYPE_CHECKING:


KEY = "hxneypxtz"
VALUE = "yum"


def as_x_on_formdata() -> dict[str,str]:
    return {"x_on_formdata": f'$event.formData.set("{KEY}", "{VALUE}")'}


def is_absent(request: HttpRequest) -> bool:
    return request.POST.get(KEY) != VALUE


def respond() -> HttpResponse:
    return HttpResponse(status=400)
