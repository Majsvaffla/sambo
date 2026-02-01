from __future__ import annotations

import typing as t

import htpy as h
from django.urls import reverse

if t.TYPE_CHECKING:
    from uuid import UUID

    class UniquelyIdentifiable(t.Protocol):
        identifier: UUID


def details_url(instance: UniquelyIdentifiable, *, title: str, url_pattern_name: str) -> h.Element:
    return h.a(href=reverse(url_pattern_name, args=[instance.identifier]), target="_blank")[
        f"{title} ", h.wa_icon(name="arrow-up-right-from-square")
    ]
