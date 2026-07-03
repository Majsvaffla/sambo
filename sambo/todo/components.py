from collections.abc import Iterable

import htpy as h
from django.http import HttpRequest
from django.templatetags.static import static
from django.urls import reverse

from sambo.components import page

from .models import CheckList, CheckListItem


def item(instance: CheckListItem) -> h.Element:
    return h.wa_input(
        {
            "@focus": '$el.appearance = "outlined"',
            "@blur": '$el.appearance = "filled"',
            "@keyup.shift.backspace": """$el.value.length == 0 && (
                $el.querySelector("wa-icon").dispatchEvent(new CustomEvent("delete-check-list-item"))
            )""",
        },
        pill=True,
        size="medium",
        appearance="filled",
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
            hx_delete=reverse("check_list_item", args=[instance.list.identifier, instance.pk]),
            hx_trigger="click,delete-check-list-item",
            hx_target="ol",
            hx_swap="innerHTML",
        )
    ]


def items(instance: CheckList) -> Iterable[h.Element]:
    for i in instance.items.order_by("-pk"):
        yield h.li[item(i)]


def check_list(request: HttpRequest, instance: CheckList) -> h.Element:
    return page(
        request,
        title=instance.name.capitalize(),
        head=[
            h.link(rel="stylesheet", href=static("todo/styles.css")),
        ],
        main=h.main(".wa-stack")[
            h.wa_card[
                h.h1(slot="header")[instance.name],
                h.form(
                    hx_post=reverse("check_list", args=[instance.identifier]),
                    hx_trigger="submit,plus-clicked",
                    hx_target="ol",
                    hx_swap="afterbegin",
                )[
                    h.wa_input(
                        {"@submit.outside": '$el.value = ""', "@plus-clicked": '$el.value = ""'},
                        name="description",
                        placeholder="Lägg till ny punkt",
                        pill=True,
                        size="medium",
                        with_clear=True,
                    )[
                        h.wa_icon(
                            {"@click": '$dispatch("plus-clicked")'},
                            slot="start",
                            name="plus",
                            variant="solid",
                        )
                    ],
                ],
                h.ol(".wa-stack.wa-gap-m")[items(instance)],
            ],
        ],
    )
