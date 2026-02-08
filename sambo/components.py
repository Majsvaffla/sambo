from __future__ import annotations

import typing as t

import htpy as h
from django.middleware import csrf
from django.templatetags.static import static
from django.urls import reverse

if t.TYPE_CHECKING:
    from uuid import UUID

    from django.http import HttpRequest

    class UniquelyIdentifiable(t.Protocol):
        identifier: UUID


def details_url(instance: UniquelyIdentifiable, *, title: str, url_pattern_name: str) -> h.Element:
    return h.a(href=reverse(url_pattern_name, args=[instance.identifier]), target="_blank")[
        f"{title} ", h.wa_icon(name="arrow-up-right-from-square")
    ]


def page(request: HttpRequest, *, title: str, main: h.Node, head: h.Node = ()) -> h.Element:
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
        h.body(hx_headers=f'{{"X-CSRFToken": "{csrf.get_token(request)}"}}', x_data="")[main],
    ]


def _page(request: HttpRequest, *content: h.Node, title: str) -> h.Element:
    return page(request, title=title, main=content)


def index_page(request: HttpRequest) -> h.Element:
    return _page(
        request,
        h.main(
            ".wa-grid.wa-gap-xl",
            x_data=r"""{
               isCheckListDialogOpen: false,
               isBillDialogOpen: false,
            }""",
        )[
            h.section[
                h.wa_button({"@click": "isCheckListDialogOpen = true"}, variant="brand", appearance="outlined")[
                    h.div(".wa-flank.wa-gap-xl")[
                        h.wa_icon(name="list-check"),
                        h.h1["Lista"],
                    ],
                ],
                h.p["Lista vardagens inköp eller resväskans innehåll"],
                h.wa_dialog(
                    {
                        ":open": "isCheckListDialogOpen",
                        "@wa-after-hide": "isCheckListDialogOpen = false",
                    }
                )[
                    h.form(".wa-stack", {"@formdata": '$event.formData.set("hxneypxtz", "yum")'})[
                        h.wa_input(label="Listans namn", name="name", required=True, autofocus=True),
                        h.wa_button(
                            variant="brand",
                            hx_post=reverse("check_list_create"),
                            hx_disabled_elt="this",
                        )["Skapa lista"],
                    ],
                ],
            ],
            h.section[
                h.wa_button(
                    {"@click": "isBillDialogOpen = true"},
                    variant="brand",
                    appearance="outlined",
                )[
                    h.div(".wa-flank.wa-gap-xl")[
                        h.wa_icon(name="coins"),
                        h.h1["Nota"],
                    ],
                ],
                h.p["Dela utgifter jämnt mellan er"],
                h.wa_dialog(
                    {
                        ":open": "isBillDialogOpen",
                        "@wa-after-hide": "isBillDialogOpen = false",
                    }
                )[
                    h.form(".wa-stack", {"@formdata": '$event.formData.set("hxneypxtz", "yum")'})[
                        h.wa_input(label="Notans namn", name="name", required=True, autofocus=True),
                        h.wa_button(
                            variant="brand",
                            hx_post=reverse("bill_create"),
                            hx_disabled_elt="this",
                        )["Skapa nota"],
                    ],
                ],
            ],
        ],
        title="Sambo",
    )
