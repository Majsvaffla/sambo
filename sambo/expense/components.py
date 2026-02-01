from collections.abc import Iterable
from datetime import date

from django.urls import reverse
import htpy as h
from django.http import HttpRequest, HttpResponse
from django.middleware import csrf
from django.templatetags.static import static
from django.utils import timezone

from .formatters import format_money
from .models import Expense, Bill


def expense(instance: Expense) -> h.Element:
    return h.tr[
        h.th(scope="row")[instance.description],
        h.td[instance.spent_at.isoformat()],
        h.td[format_money(instance.amount)],
    ]


def expenses(instance: Bill, settled_at: date) -> Iterable[h.Element]:
    for i in instance.expenses.filter(settled_at__gt=settled_at).order_by("-spent_at"):
        yield expense(i)


def expense_form(instance: Bill) -> h.Element:
    return h.wa_card[
        h.form[
            h.wa_input(type="text", label="Beskrivning"),
            h.wa_input(type="date", label="Spenderad"),
            h.wa_input(type="number", label="Summa"),
        ]
    ]
def bill(request: HttpRequest, instance: Bill, settled_at: date) -> HttpResponse:
    unsettled_amount = instance.sum_unsettled_amount_at(settled_at)
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
                h.link(rel="stylesheet", href=static("expense/styles.css")),
                h.script(type="module", src=static("vendor/webawesome/webawesome.loader.js")),
                h.script(defer=True, src=static("vendor/alpinejs.min.js")),
                h.script(defer=True, src=static("vendor/htmx.min.js")),
                h.script(src=static("script.js")),
            ],
            h.body(hx_headers=f'{{"X-CSRFToken": "{csrf.get_token(request)}"}}', x_data="")[
                h.main(".wa-stack")[
                    h.wa_card[
                        h.h1(slot="header")[instance.name],
                        h.section[
                            h.wa_button(
                                variant="brand",
                                appearance="outlined",
                                size="small",
                                icon="plus",
                                pill=True,
                                hx_get=reverse("expense_create", args=[instance.identifier]),
                                hx_target="closest wa-card",
                                hx_swap="outerHTML"
                            )[
                                h.wa_icon(slot="start", name="plus"),
                                "Lägg till utgift",
                            ],
                            h.table[
                                h.caption[f"Ej uppgjorda utgifter sedan {settled_at.isoformat()}"],
                                h.thead[
                                    h.tr[
                                        h.th(scope="col")["Beskrivning"],
                                        h.th(scope="col")["Datum"],
                                        h.th(scope="col")["Summa"],
                                    ],
                                ],
                                h.tbody[
                                    expenses(instance, settled_at),
                                ],
                                h.tfoot[
                                    h.tr[
                                        h.th(scope="row", colspan="2")["Totalt"],
                                        h.td[format_money(unsettled_amount)],
                                    ],
                                ],
                            ],
                        ],
                        h.section(slot="footer")[
                            h.p[f"Att betala: {format_money(unsettled_amount / 2)}"],
                            h.wa_button(
                                slot="footer-actions",
                                variant="brand",
                                hx_patch=reverse("bill_settled_at", args=[instance.identifier, settled_at]),
                                hx_target="closest wa-card",
                                hx_swap="outerHTML",
                            )["Gör upp"],
                        ],
                    ]
                ]
            ],
        ]
    )
