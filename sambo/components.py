from __future__ import annotations

import typing as t

import htpy as h
from django.middleware import csrf
from django.templatetags.static import static
if t.TYPE_CHECKING:
    from django.http import HttpRequest


def page(request: HttpRequest, *, title: str, main: h.Node, head: h.Node) -> h.Element:
    return h.html(".wa-theme-awesome.wa-brand-blue.wa-cloak", lang="sv")[
        h.head[
            h.meta(charset="utf-8"),
            h.meta(
                name="viewport",
                content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover",
            ),
            h.title[title],
            h.style[
                # Avoid Flash of Undefined Custom Elements (FOUCE):
                # https://www.abeautifulsite.net/posts/flash-of-undefined-custom-elements/
                ":not(:defined) { visibility: hidden; }"
            ],
            h.link(rel="stylesheet", href=static("styles.css")),
            h.link(rel="stylesheet", href=static("vendor/webawesome/styles/webawesome.css")),
            h.link(rel="stylesheet", href=static("vendor/webawesome/styles/themes/awesome.css")),
            h.script(type="module", src=static("vendor/webawesome/webawesome.loader.js")),
            h.script(defer=True, src=static("script.js")),
            h.script(defer=True, src=static("vendor/alpinejs.min.js")),
            h.script(defer=True, src=static("vendor/htmx.min.js")),
            head,
        ],
        h.body(hx_headers=f'{{"X-CSRFToken": "{csrf.get_token(request)}"}}', x_data="")[h.main(".wa-stack")[main]],
    ]
