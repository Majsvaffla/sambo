from collections.abc import Iterable

import htpy as h
from django.http import HttpRequest, HttpResponse
from django.middleware import csrf
from django.templatetags.static import static
from django.urls import reverse

from .models import CheckListItem, CheckList


def item(instance: CheckListItem) -> h.Element:
    return h.wa_input(
        {
            "@focus": '$el.appearance = "outlined"',
            "@blur": '$el.appearance = "filled"',
        },
        pill=True,
        size="medium",
        appearance="filled",
        style="min-width: 332px",
        value=instance.description,
        name="description",
        hx_post=reverse("check_list_item", args=[instance.list.identifier, instance.pk]),
        hx_trigger="blur changed,click[enterKey] changed",
        hx_swap="outerHTML",
    )[
        h.wa_icon(
            slot="start",
            name="minus",
            variant="solid",
            style="color: black",
            hx_delete=reverse("check_list_item", args=[instance.list.identifier, instance.pk]),
            hx_target="ol",
            hx_swap="innerHTML",
        )
    ]


def items(instance: CheckList) -> Iterable[h.Element]:
    for i in instance.items.order_by("-pk"):
        yield h.li[item(i)]


def check_list(request: HttpRequest, instance: CheckList) -> HttpResponse:
    return HttpResponse(
        h.html(".wa-theme-awesome.wa-brand-blue.wa-cloak", lang="sv")[
            h.head[
                h.meta(charset="utf-8"),
                h.meta(
                    name="viewport",
                    content="width=device-width, initial-scale=1.0, user-scalable=no, viewport-fit=cover",
                ),
                h.title[instance.name.capitalize()],
                h.style[
                    # Avoid Flash of Undefined Custom Elements (FOUCE):
                    # https://www.abeautifulsite.net/posts/flash-of-undefined-custom-elements/
                    ":not(:defined) { visibility: hidden; }"
                ],
                h.link(rel="stylesheet", href=static("vendor/webawesome/styles/webawesome.css")),
                h.link(rel="stylesheet", href=static("vendor/webawesome/styles/themes/awesome.css")),
                h.script(type="module", src=static("vendor/webawesome/webawesome.loader.js")),
                h.script(defer=True, src=static("vendor/alpinejs.min.js")),
                h.script(defer=True, src=static("vendor/htmx.min.js")),
            ],
            h.body(hx_headers=f'{{"X-CSRFToken": "{csrf.get_token(request)}"}}', x_data="")[
                h.main(".wa-stack", style="align-items: center")[
                    h.section(".wa-card", style="max-width: 512px")[
                        h.h1(slot="header")[instance.name],
                        h.form(
                            style="margin-bottom: var(--wa-space-m)",
                            hx_post=reverse("check_list", args=[instance.identifier]),
                            hx_trigger="submit",
                            hx_target="ol",
                            hx_swap="afterbegin",
                        )[
                            h.wa_input(
                                {"@submit.outside": '$el.value = ""'},
                                name="description",
                                placeholder="Lägg till ny punkt",
                                pill=True,
                                size="medium",
                                with_clear=True,
                                style="min-width: 332px",
                            )[
                                h.wa_icon(
                                    slot="start",
                                    name="plus",
                                    variant="solid",
                                    style="color: black",
                                )
                            ],
                        ],
                        h.ol(".wa-stack.wa-gap-m", style="list-style: none; margin-inline-start: 0")[items(instance)],
                    ]
                ]
            ],
        ]
    )
