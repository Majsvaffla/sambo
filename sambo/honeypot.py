from __future__ import annotations

import json
import typing as t

from django.http import HttpRequest, HttpResponse

if t.TYPE_CHECKING:
    type HoneyPotKey = t.Literal["hxneypxtz"]
    type HoneyPotValue = t.Literal["yum"]

    class HoneyPotDict(t.TypedDict):
        hxneypxtz: t.Literal[HoneyPotValue]


def as_hx_vals() -> dict[str, str]:
    return json.dumps(as_dict())


def as_dict() -> HoneyPotDict:
    return {"hxneypxtz": "yum"}


[(_key, _value)] = as_dict().items()


def is_absent(request: HttpRequest) -> bool:
    return request.POST.get(_key) != _value


def respond() -> HttpResponse:
    return HttpResponse(status=400)
